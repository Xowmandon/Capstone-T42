//
//  GameObject.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation

struct GameObject : Identifiable {
    
    static let gameList : [GameObject] = [GameObject(name: "Red Flag Racing"), GameObject(name: "Heartfall"), GameObject(name: "Tic-Tac-Toe"), GameObject(name: "RPG Battle")]
        let id : UUID = UUID()
        let name : String
        let imageName : String = "gamecontroller.circle.fill"
        
}

struct GameState : Codable {
    
    let gameName : String
    
}
