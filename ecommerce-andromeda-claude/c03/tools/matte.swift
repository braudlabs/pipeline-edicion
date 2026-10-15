// Mattes de sujeto con Vision (macOS), sin modelos descargados.
//
// Lee un vídeo fotograma a fotograma con AVAssetReader (índice de muestra = índice de
// fotograma fuente), segmenta y escribe un PNG por fotograma: blanco + alfa = sujeto.
//
//   swift tools/matte.swift <video> <outDir> <first> <last> [person|foreground] [scale]
//
// person      VNGeneratePersonSegmentationRequest (.accurate): todas las personas.
// foreground  VNGenerateForegroundInstanceMaskRequest: instancias de primer plano.
// scale       factor de salida (1 = 1080×1920). Los fotogramas fuera de rango no se procesan.
import AVFoundation
import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

let args = CommandLine.arguments
guard args.count >= 5 else {
    print("uso: matte.swift <video> <outDir> <first> <last> [person|foreground] [scale]")
    exit(2)
}
let url = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
let first = Int(args[3])!
let last = Int(args[4])!
let mode = args.count > 5 ? args[5] : "person"
let scale = args.count > 6 ? Double(args[6])! : 1.0
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

let ctx = CIContext(options: [.workingColorSpace: NSNull()])
let asset = AVURLAsset(url: url)
let semaphore = DispatchSemaphore(value: 0)
var track: AVAssetTrack?
Task {
    track = try? await asset.loadTracks(withMediaType: .video).first
    semaphore.signal()
}
semaphore.wait()
guard let videoTrack = track else { print("sin pista de vídeo"); exit(1) }
let reader = try AVAssetReader(asset: asset)
let output = AVAssetReaderTrackOutput(track: videoTrack, outputSettings: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
])
output.alwaysCopiesSampleData = false
reader.add(output)
reader.startReading()

func writeMask(_ mask: CIImage, width: Int, height: Int, index: Int) throws {
    // mask: luminancia 0..1 a tamaño de imagen. Salida RGBA: blanco con alfa = máscara.
    let w = Int((Double(width) * scale).rounded()), h = Int((Double(height) * scale).rounded())
    let sx = Double(w) / mask.extent.width, sy = Double(h) / mask.extent.height
    let scaled = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
    let white = CIImage(color: .white).cropped(to: CGRect(x: 0, y: 0, width: w, height: h))
    let clear = CIImage(color: .clear).cropped(to: CGRect(x: 0, y: 0, width: w, height: h))
    let blended = white.applyingFilter("CIBlendWithMask", parameters: [
        kCIInputBackgroundImageKey: clear,
        kCIInputMaskImageKey: scaled,
    ])
    let path = outDir.appendingPathComponent(String(format: "m%04d.png", index))
    guard let cg = ctx.createCGImage(blended, from: CGRect(x: 0, y: 0, width: w, height: h), format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { throw NSError(domain: "matte", code: 1) }
    guard let dest = CGImageDestinationCreateWithURL(path as CFURL, UTType.png.identifier as CFString, 1, nil) else { throw NSError(domain: "matte", code: 2) }
    CGImageDestinationAddImage(dest, cg, nil)
    CGImageDestinationFinalize(dest)
}

var index = 0
var written = 0
let started = Date()
while let sample = output.copyNextSampleBuffer() {
    defer { index += 1 }
    if index < first { continue }
    if index > last { break }
    guard let pixel = CMSampleBufferGetImageBuffer(sample) else { continue }
    let width = CVPixelBufferGetWidth(pixel), height = CVPixelBufferGetHeight(pixel)
    let handler = VNImageRequestHandler(cvPixelBuffer: pixel, options: [:])
    var maskImage: CIImage?
    if mode == "foreground" {
        let request = VNGenerateForegroundInstanceMaskRequest()
        try handler.perform([request])
        if let result = request.results?.first {
            let buffer = try result.generateScaledMaskForImage(forInstances: result.allInstances, from: handler)
            maskImage = CIImage(cvPixelBuffer: buffer)
        }
    } else {
        let request = VNGeneratePersonSegmentationRequest()
        request.qualityLevel = .accurate
        request.outputPixelFormat = kCVPixelFormatType_OneComponent8
        try handler.perform([request])
        if let buffer = request.results?.first?.pixelBuffer {
            maskImage = CIImage(cvPixelBuffer: buffer)
        }
    }
    let mask = maskImage ?? CIImage(color: .black).cropped(to: CGRect(x: 0, y: 0, width: width, height: height))
    // Llevar la máscara al tamaño del fotograma antes de escribir.
    let fitted = mask.transformed(by: CGAffineTransform(scaleX: Double(width) / mask.extent.width, y: Double(height) / mask.extent.height))
    try writeMask(fitted, width: width, height: height, index: index)
    written += 1
}
print("mattes: \(written) fotogramas \(first)–\(last) en \(String(format: "%.1f", Date().timeIntervalSince(started))) s · modo \(mode)")
