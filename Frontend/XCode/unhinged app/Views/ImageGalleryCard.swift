//
//  ImageGalleryCard.swift
//  unhinged app
//
//  Created by Harry Sho on 3/31/25.
//

import Foundation
import SwiftUI

struct ImageGalleryCard : View {
    
    let image : Image = Image(systemName: "photo.fill")
    let title : String = "Title"
    let description : String = "Very descriptive"
    
    var body: some View {
        CardBackground()
            .overlay{
                VStack (spacing: 5) {
                    image
                        .resizable()
                        .mask(Rectangle())
                    Text(title)
                        .font(Theme.headerFont)
                    Text(description)
                        .font(Theme.captionFont)
                }
                .padding()
            }
    }
    
}
