import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers
let input=CommandLine.arguments[1],out=CommandLine.arguments[2]
let fm=FileManager.default
let files=try fm.contentsOfDirectory(atPath:input).filter{$0.hasSuffix(".png")}.sorted()
let ctx=CIContext(options:[.useSoftwareRenderer:false])
let req=VNGeneratePersonSegmentationRequest();req.qualityLevel = .accurate;req.outputPixelFormat=kCVPixelFormatType_OneComponent8
for file in files {
 try autoreleasepool {
  let url=URL(fileURLWithPath:input+"/"+file)
  guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),let cg=CGImageSourceCreateImageAtIndex(src,0,nil) else {throw NSError(domain:"image",code:1)}
  try VNImageRequestHandler(cgImage:cg,options:[:]).perform([req])
  guard let buffer=req.results?.first?.pixelBuffer else {throw NSError(domain:"mask",code:2)}
  let ci=CIImage(cvPixelBuffer:buffer);let resized=ci.transformed(by:CGAffineTransform(scaleX:CGFloat(cg.width)/ci.extent.width,y:CGFloat(cg.height)/ci.extent.height))
  try ctx.writePNGRepresentation(of:resized,to:URL(fileURLWithPath:out+"/"+file),format:.L8,colorSpace:CGColorSpaceCreateDeviceGray(),options:[:])
  print(file)
 }
}
