import Foundation
import Vision
import AppKit
let dir=URL(fileURLWithPath:CommandLine.arguments[1])
let paths=try FileManager.default.contentsOfDirectory(at:dir,includingPropertiesForKeys:nil).filter{$0.pathExtension=="jpg"}.sorted{$0.lastPathComponent<$1.lastPathComponent}
var output:[[String:Any]]=[]
for url in paths {
 autoreleasepool {
  guard let img=NSImage(contentsOf:url), let cg=img.cgImage(forProposedRect:nil,context:nil,hints:nil) else {return}
  let r=VNDetectFaceRectanglesRequest()
  do {
   try VNImageRequestHandler(cgImage:cg,options:[:]).perform([r])
   let boxes=(r.results ?? []).map {o -> [String:Double] in let b=o.boundingBox;return ["x":b.minX*1080,"y":(1-b.maxY)*1920,"w":b.width*1080,"h":b.height*1920,"confidence":Double(o.confidence)]}
   output.append(["file":url.lastPathComponent,"faces":boxes])
  } catch {output.append(["file":url.lastPathComponent,"error":"\(error)"])}
 }
}
let data=try JSONSerialization.data(withJSONObject:output,options:[.prettyPrinted,.sortedKeys]);FileHandle.standardOutput.write(data)
