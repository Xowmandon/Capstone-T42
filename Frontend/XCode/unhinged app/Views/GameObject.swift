//
//  GameObject.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation

struct GameObject : Identifiable {
    
    static let gameList : [GameObject] = [GameObject(name: "Red Flag Racing"), GameObject(name: "Heartfall"), GameObject(name: "RPG Battle"), GameObject(name: "Flag Match") ]
        let id : UUID = UUID()
        let name : String
        let imageName : String = "gamecontroller.circle.fill"
        
}
