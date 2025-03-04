//
//  func.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import SwiftUI

struct ProfileCard : View {
    
    //let editable : Bool
    
    //let profile : Profile
    let profileImage : Image
    let name : String
    let age : Int
    let theme : Theme = Theme.shared
    var body: some View {
        ZStack {
            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
            
            //Profile Image
            GeometryReader { geometry in
                profileImage
                    .resizable()
                    .scaledToFill()
                    .clipped()
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .mask(Rectangle())
                    .overlay(alignment: .bottomTrailing){
                        
                        
                            
                            //TODO: Photo Picker
                            
                        
                    }
            }
            .padding(5)
            VStack {
                Spacer()
                
                //Profile Information
                VStack {
                    HStack(spacing: 20){
                        Text(self.name)
                            .font(Theme.bodyFont)
                        //.font(.system(.largeTitle, weight: .bold))
                        //.offset(x: -2)
                        Spacer()
                        Text("\(age)")
                            .font(Theme.bodyFont)
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
