//
//  Message.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

struct Message : Identifiable, Codable {
    
    enum Kind : String, Codable {
        case text = "text"
        case game = "game"
    }
    let id : UUID = UUID()
    
    var kind : Kind
    var content : String = ""
    var sentFromClient : Bool = false
    
    //private var gameState : GameState?
    
    enum CodingKeys: String, CodingKey {
        case kind
        case content
        case sentFromClient = "sentFromClient"
    }
    
}

struct MessageResponse: Codable {
    
    let matchId : String
    let messages: [Message]
    //let totalMessages: Int
    
    enum CodingKeys: String, CodingKey {
        case matchId = "match_id"
        case messages
        //case totalMessages = "total_messages"
    }
    
    
}
