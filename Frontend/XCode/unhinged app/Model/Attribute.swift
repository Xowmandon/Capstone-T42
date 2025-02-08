//
//  Attribute.swift
//  unhinged app
//
//  Created by Harry Sho on 2/8/25.
//

import Foundation

struct Attribute : Identifiable, Hashable {
    
    var id : UUID = UUID()
    let customName : String
    let symbolName : String
    
    init(customName : String, symbolName : String) {
        self.customName = customName
        self.symbolName = symbolName
    }
    
}
