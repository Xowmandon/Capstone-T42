//
//  ImageGalleryCard.swift
//  unhinged app
//
//  Created by Harry Sho on 3/31/25.
//

import Foundation
import SwiftUI
import PhotosUI

struct ImageGalleryCard : View {
    
    let isEditable : Bool
    @Binding var galleryItem : ImageGalleryItem
    
    @State var image : Image = Image(systemName: "photo.fill")
    @State var title : String = "Title"
    @State var description : String = "Very descriptive"
    
    @State var imageItem: PhotosPickerItem?
    @State var isLoadingImage : Bool = false
    //@Binding var isFocused: BuildProfileFocusedField?
    
    var body: some View {
        VStack (spacing: 5) {
        
            VStack {
                if isLoadingImage {
                    ProgressView("Loading your image...")
                }
                GeometryReader { geometry in
                    image
                        .resizable()
                        .scaledToFill()
                        .clipped()
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .mask(Rectangle())
                        .overlay(alignment: .bottomTrailing){
                            if isEditable {
                                PhotosPicker(selection: $imageItem,
                                             matching: .images,
                                             photoLibrary: .shared()) {
                                    Image(systemName: "photo.badge.plus")
                                        .symbolRenderingMode(.monochrome)
                                        .font(.system(size: 30))
                                        .padding()
                                        .background {
                                            CardBackground()
                                        }
                                }
                                .onChange(of: imageItem) {
                                    Task {
                                        isLoadingImage = true
                                        if let imgData = try? await imageItem?.loadTransferable(type: Data.self) {
                                            let uiImg = UIImage(data: imgData)
                                            image = Image(uiImage: uiImg!)
                                            galleryItem.image = Image(uiImage: uiImg!)
                                            isLoadingImage = false
                                        } else {
                                            print("Failed")
                                        }
                                    }
                                }
                            }
                        }
                }
                .frame(minHeight: 300)
            }
            .padding()
            VStack {
                if isEditable {
                    HStack {
                        Image(systemName: "pencil")
                            .foregroundStyle(.secondary)
                        TextField("Title",text: $galleryItem.title)
                            .lineLimit(1)
                            .font(Theme.titleFont)
                            //.focused($isFocused, equals: BuildProfileFocusedField.gallery)
                    }
                    HStack {
                        Image(systemName: "pencil")
                            .foregroundStyle(.secondary)
                        TextField("Describe your gallery item...", text: $galleryItem.description)
                            .lineLimit(3, reservesSpace: true) // Always reserves space for 3 lines
                            .font(Theme.bodyFont)
                            //.focused($isFocused, equals: BuildProfileFocusedField.gallery)
                    }
                } else {
                    Text(galleryItem.title)
                        .lineLimit(1)
                        .font(Theme.headerFont)
                    Text(galleryItem.description)
                        .lineLimit(3, reservesSpace: true)
                        .font(Theme.captionFont)
                }
            }
            .padding(.horizontal)
            .padding(.bottom)
        }
        .background{
            CardBackground()
        }
    }
    
}

struct GalleryCard : View {

    let image : Image
    let title : String
    let description : String
    
    var body: some View {
        VStack (spacing: 5) {
        
            VStack {
                GeometryReader { geometry in
                    image
                        .resizable()
                        .scaledToFill()
                        .clipped()
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .mask(Rectangle())
                }
                .frame(minHeight: 300)
            }
            .padding()
            VStack {
                Text(title)
                    .font(Theme.headerFont)
                Text(description)
                    .font(Theme.captionFont)
            }
            .padding(.horizontal)
            .padding(.bottom)
        }
        .background{
            CardBackground()
        }
        
    }

}
