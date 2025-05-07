//
//  CreateGalleryItem.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/23/25.
//

import Foundation

import SwiftUI

struct CreateGalleryItem: View {
    @Binding var presentationMode : PresentationMode
    @Binding var gallery : [ImageGalleryItem]
    @State var galleryItem : ImageGalleryItem = ImageGalleryItem()
    
    var body: some View {
        VStack {
            HStack{
                BackButton()
                Spacer()
                Text("Add a Gallery Entry")
                    .font(Theme.titleFont)
                Spacer()
            }
            .padding()
            VStack {
                ImageGalleryCard(isEditable: true, galleryItem: $galleryItem)
                Button {
                    saveGalleryItem()
                    presentationMode.dismiss()
                } label: {
                    Text("Confirm")
                        .font(Theme.bodyFont)
                        .foregroundStyle(.blue)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background{CardBackground()}
                    
                }
            }
            .padding()
        }
    }
    
    func saveGalleryItem(){
        gallery.append(galleryItem)
    }
}
