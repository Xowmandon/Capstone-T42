//
//  Message.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

struct Message : Identifiable {
    
    enum Kind : String, Codable {
        case text
        case game
    }
    
    var kind : Kind = Kind.text
    var id : String = UUID().uuidString
    var content : String = "Hello world"
    
    //private var gameState : GameState?
    
}
