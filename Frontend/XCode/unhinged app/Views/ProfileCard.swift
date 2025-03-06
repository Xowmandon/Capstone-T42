//
//  func.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI
import PhotosUI

struct ProfileCard : View {
    @State var profileImageItem : PhotosPickerItem?
    
    @Binding var profileImage : Image
    @Binding var name : String
    @Binding var age : Int
    var isEditable : Bool = false
    
    @FocusState.Binding var focusedField : BuildProfileFocusedField?
    
    let theme : Theme = Theme.shared
    var body: some View {
        VStack (spacing: 0){
            //Profile Image
            GeometryReader { geometry in
                profileImage
                    .resizable()
                    .scaledToFill()
                    .clipped()
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .mask(Rectangle())
                    .overlay(alignment: .bottomTrailing){
                        if isEditable {
                            PhotosPicker(selection: $profileImageItem,
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
                            .onChange(of: profileImageItem) {
                                Task {
                                    if let imgData = try? await profileImageItem?.loadTransferable(type: Data.self) {
                                        let uiImg = UIImage(data: imgData)
                                        profileImage = Image(uiImage: uiImg!)
                                    } else {
                                        print("Failed")
                                    }
                                }
                            }
                        }
                    }
            }
            .padding(5)
            .background{
                CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
            }
            //Profile Info
            HStack(spacing: 10){
                if isEditable{
                    Image(systemName: "pencil")
                        .foregroundStyle(.secondary)
                    TextField("Name", text: $name)
                        .focused($focusedField, equals: .name)
                        .font(Theme.headerFont)
                        .background(Color(.quaternarySystemFill))
                    Spacer()
                    Text("Age:")
                        .font(Theme.headerFont)
                    Picker("",selection: $age) {
                        ForEach(18..<101, id: \.self) { age in
                            Text("\(age)").tag(age)
                        }
                    }
                    .pickerStyle(.menu)
                    
                }else{
                    Text(self.name)
                        .font(Theme.headerFont)
                    Spacer()
                    Text("\(age)")
                        .font(Theme.headerFont)
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

#Preview {
    
    @Previewable @State var profileImage : Image = Image(systemName: "person.fill")
    @Previewable @State var name : String = "John Doe"
    @Previewable @State var age : Int = 24
    @Previewable @FocusState var focusedField : BuildProfileFocusedField?
    
    ProfileCard(profileImage: $profileImage, name: $name, age: $age, isEditable: true, focusedField: $focusedField)
}
