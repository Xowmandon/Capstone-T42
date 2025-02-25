//
//  func.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import SwiftUI

struct ProfileCard : View {
    
    let profile : Profile
    
    let theme : Theme = Theme.shared
    
    var body: some View {
        
        ZStack {
            
            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
            
            //Profile Image
            
            GeometryReader { geometry in
                
                Image(profile.imageName)
                    .resizable()
                    .scaledToFill()
                    .clipped()
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .mask(Rectangle())
                
            }
            .padding(5)
            
            VStack {
                
                Spacer()
                
                //Profile Information
                
                VStack {
                    
                    HStack(spacing: 20){
                        
                        Text(profile.name)
                            .font(Theme.titleFont)
                        //.font(.system(.largeTitle, weight: .bold))
                        //.offset(x: -2)
                        Spacer()
                        Text("21")
                            .font(Theme.titleFont)
                        
                        
                    }
                    
                }
                .padding(.horizontal, 30)
                .padding(.vertical, 30)
                .background{
                    
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    
                }
                
                
            }
        }
        
    }
}
