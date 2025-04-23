//
//  ImageGalleryItem.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/23/25.
//

import Foundation
import SwiftUI

struct ImageGalleryItem : Identifiable {
    
    let id : UUID = UUID()
    
    var image : Image = Image(systemName: "photo.fill")
    var title : String = "Title"
    var description : String = "A very descriptive description of your image.."
    
}
