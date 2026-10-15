// Lee un vídeo fotograma a fotograma y vuelca, por fotograma, el texto en pantalla
// (con su cuadrilátero y la caja de cada palabra) y las caras (caja y pupilas).
// Usa el framework Vision de macOS: todo local, sin red.
//
//   visionscan <video> <salida.jsonl> [--step N] [--from F] [--to F] [--fast] [--nofaces]
//
// Coordenadas en píxeles del fotograma, origen arriba a la izquierda.

import AVFoundation
import Foundation
import Vision

var args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else {
    FileHandle.standardError.write("uso: visionscan <video> <salida.jsonl> [--step N] [--from F] [--to F] [--fast] [--nofaces]\n".data(using: .utf8)!)
    exit(2)
}
let videoURL = URL(fileURLWithPath: args[0])
let outURL = URL(fileURLWithPath: args[1])
var step = 1
var fromF = 0
var toF = Int.max
var fast = false
var wantFaces = true
var i = 2
while i < args.count {
    switch args[i] {
    case "--step": step = Int(args[i + 1])!; i += 1
    case "--from": fromF = Int(args[i + 1])!; i += 1
    case "--to": toF = Int(args[i + 1])!; i += 1
    case "--fast": fast = true
    case "--nofaces": wantFaces = false
    default: break
    }
    i += 1
}

let asset = AVURLAsset(url: videoURL)
guard let track = asset.tracks(withMediaType: .video).first else { fatalError("sin pista de vídeo") }
let fps = Double(track.nominalFrameRate)
let size = track.naturalSize
let W = Double(size.width), H = Double(size.height)

let reader = try AVAssetReader(asset: asset)
let output = AVAssetReaderTrackOutput(
    track: track,
    outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
output.alwaysCopiesSampleData = false
reader.add(output)
reader.startReading()

FileManager.default.createFile(atPath: outURL.path, contents: nil)
let out = try FileHandle(forWritingTo: outURL)

func r(_ v: Double) -> Double { (v * 10).rounded() / 10 }
// Vision: normalizado, origen abajo a la izquierda -> píxeles, origen arriba a la izquierda.
func px(_ p: CGPoint) -> [Double] { [r(Double(p.x) * W), r((1 - Double(p.y)) * H)] }
func box(_ b: CGRect) -> [Double] {
    [r(Double(b.minX) * W), r((1 - Double(b.maxY)) * H), r(Double(b.width) * W), r(Double(b.height) * H)]
}

var n = 0
var done = 0
while let sb = output.copyNextSampleBuffer() {
    defer { n += 1 }
    if n < fromF || n > toF || (n - fromF) % step != 0 { continue }
    guard let pb = CMSampleBufferGetImageBuffer(sb) else { continue }
    let pts = CMSampleBufferGetPresentationTimeStamp(sb).seconds

    let textReq = VNRecognizeTextRequest()
    textReq.recognitionLevel = fast ? .fast : .accurate
    textReq.usesLanguageCorrection = false
    textReq.recognitionLanguages = ["es-ES", "en-US"]
    textReq.minimumTextHeight = 0.006
    var reqs: [VNRequest] = [textReq]
    let faceReq = VNDetectFaceLandmarksRequest()
    if wantFaces { reqs.append(faceReq) }

    let handler = VNImageRequestHandler(cvPixelBuffer: pb, orientation: .up, options: [:])
    do { try handler.perform(reqs) } catch { continue }

    var texts: [[String: Any]] = []
    for obs in textReq.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        let s = cand.string
        var words: [[String: Any]] = []
        var searchStart = s.startIndex
        for w in s.split(separator: " ") {
            guard let rg = s.range(of: String(w), range: searchStart..<s.endIndex) else { continue }
            searchStart = rg.upperBound
            if let wb = try? cand.boundingBox(for: rg) {
                words.append(["s": String(w), "b": box(wb.boundingBox)])
            }
        }
        texts.append([
            "s": s,
            "c": (Double(cand.confidence) * 100).rounded() / 100,
            "q": px(obs.topLeft) + px(obs.topRight) + px(obs.bottomRight) + px(obs.bottomLeft),
            "words": words,
        ])
    }

    var faces: [[String: Any]] = []
    if wantFaces {
        for f in faceReq.results ?? [] {
            var d: [String: Any] = ["b": box(f.boundingBox)]
            if let roll = f.roll { d["roll"] = r(roll.doubleValue * 180 / .pi) }
            if let yaw = f.yaw { d["yaw"] = r(yaw.doubleValue * 180 / .pi) }
            if let lm = f.landmarks {
                // puntos normalizados a la caja de la cara
                func abs(_ region: VNFaceLandmarkRegion2D?) -> [Double]? {
                    guard let p = region?.normalizedPoints.first else { return nil }
                    let bb = f.boundingBox
                    return px(CGPoint(x: bb.minX + CGFloat(p.x) * bb.width, y: bb.minY + CGFloat(p.y) * bb.height))
                }
                if let le = abs(lm.leftPupil) { d["le"] = le }
                if let re = abs(lm.rightPupil) { d["re"] = re }
            }
            faces.append(d)
        }
    }

    let rec: [String: Any] = ["f": n, "t": (pts * 100000).rounded() / 100000, "texts": texts, "faces": faces]
    let data = try JSONSerialization.data(withJSONObject: rec, options: [.sortedKeys])
    out.write(data)
    out.write("\n".data(using: .utf8)!)
    done += 1
    if done % 200 == 0 {
        FileHandle.standardError.write("\(videoURL.lastPathComponent): \(done) fotogramas (f\(n))\n".data(using: .utf8)!)
    }
}
try out.close()
FileHandle.standardError.write("\(videoURL.lastPathComponent): fin, \(done) fotogramas, \(fps) fps, \(Int(W))x\(Int(H))\n".data(using: .utf8)!)
