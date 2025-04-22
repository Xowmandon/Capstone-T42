//
//  Message.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

struct Message : Identifiable, Codable {
    
    enum Kind : String, Codable {
        case text
        case game
    }
    
    var kind : Kind = Kind.text
    var id : String = UUID().uuidString
    var content : String = "Hello world"
    var sentFromClient : Bool = false
    
    //private var gameState : GameState?
    
}

struct MessageResponse: Codable {
    
    let matchId : String
    let messages: [Message]
    let totalMessages: Int
    
    enum CodingKeys: String, CodingKey {
        case matchId = "match_id"
        case messages
        case totalMessages = "total_messages"
    }
    
    
}
