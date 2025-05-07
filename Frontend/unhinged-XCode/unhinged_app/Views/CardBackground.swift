//
//  CardBackground.swift
//  unhinged app
//
//  Created by Harry Sho on 2/6/25.
//

import Foundation
import SwiftUI

struct CardBackground : View {
    
    var borderColor : Color = Color(.gray)
    var innerColor : Color = Color (.white)
    
    var body: some View{
        
        Rectangle()
            .shadow(radius: 0, x: 5, y: 5)
            .foregroundStyle(borderColor)
            .overlay{
                
                Rectangle()
                    .foregroundStyle(innerColor)
                    .padding(5)
                
            }
        
    }
    
}

#Preview{
    
    CardBackground(borderColor: .blue, innerColor: .red)
        .frame(maxWidth: 100, maxHeight: 100)
    
}
