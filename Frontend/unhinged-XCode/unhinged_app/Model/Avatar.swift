//
//  Avatar.swift
//  unhinged app
//
//  Created by Harry Sho on 3/6/25.
//

struct Avatar : Codable {
    var head : headType
    var top : topType
    var bottom : bottomType
    
    enum headType : String, Codable {
        case hair1 = "hair1Sprite"
        case hair2 = "hair2Sprite"
        case hair3 = "hair3Sprite"
    }
    enum topType : String, Codable {
        case top1 = "top1Sprite"
        case top2 = "top22Sprite"
        case top3 = "top3Sprite"
    }
    enum bottomType : String, Codable {
        case bottom1 = "bottom1Sprite"
        case bottom2 = "bottom2Sprite"
        case bottom3 = "bottom3Sprite"
    }
}
