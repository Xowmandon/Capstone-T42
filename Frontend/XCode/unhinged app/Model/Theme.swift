//
//  Theme.swift
//  unhinged app
//
//  Created by Harry Sho on 2/8/25.
//

import Foundation
import SwiftUI

struct Theme {
    
    static let shared = Theme(borderColor: .gray, innerColor: .white) // Default theme
    static let titleFont : Font = Font.custom("PixelifySans-Medium", size: 32)
    static let headerFont : Font = Font.custom("PixelifySans-SemiBold", size: 24)
    static let bodyFont : Font = Font.custom("PixelifySans-Regular", size: 18)
    static let defaultBorderColor : Color = .gray
    static let defaultInnerColor : Color = .white
    
    let cardBorderColor : Color
    let cardInnerColor : Color
    
    init(borderColor : Color, innerColor : Color){
        
        self.cardBorderColor = borderColor
        self.cardInnerColor = innerColor
        
    }
    
}
