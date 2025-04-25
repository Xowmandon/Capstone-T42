//
//  Avatar.swift
//  unhinged app
//
//  Created by Harry Sho on 3/6/25.
//

import SwiftUI
import Foundation

// Author: Allison Tang
// edited by harry
struct Avatar: Codable {
    var body: BodyType
    var hair: HairType
    var top: TopType
    var bottom: BottomType
    var face: FaceType
    
    enum BodyType: String, CaseIterable, Codable {
        case skin1 = "body_skintone1"
        case skin2 = "body_skintone2"
        case skin3 = "body_skintone3"
        case skin4 = "body_skintone4"
        case skin5 = "body_skintone5"
    }
    
    enum HairType: String, CaseIterable, Codable {
        case longBlonde = "hair_long_blonde"
        case longBrown = "hair_long_brown"
        case longBlack = "hair_long_black"
        case shortBlonde = "hair_short_blonde"
        case shortBrown = "hair_short_brown"
        case shortBlack = "hair_short_black"
    }
    
    enum TopType: String, CaseIterable, Codable {
        case tshirt = "top_tshirt"
        case hoodie = "top_hoodie"
        case sweatshirt = "top_sweatshirt"
    }
    
    enum BottomType: String, CaseIterable, Codable {
        case jeans = "bottom_jeans"
        case shorts = "bottom_shorts"
        case dress = "bottom_dress"
    }
    
    enum FaceType: String, CaseIterable, Codable {
        case plain = "face_plain"
        case blush = "face_blush"
    }
}

struct AvatarCreator: View {
    @Binding var profileAvatar : Avatar
    @State private var avatar = Avatar(
        body: .skin3,
        hair: .shortBrown,
        top: .hoodie,
        bottom: .jeans,
        face: .plain
    )
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                AvatarPreview(avatar: avatar)
                    .padding()
                
                ScrollView {
                    AvatarSection(title: "Body") {
                        ForEach(Avatar.BodyType.allCases, id: \.self) { body in
                            AvatarOption(imageName: body.rawValue, isSelected: avatar.body == body) {
                                avatar.body = body
                            }
                        }
                    }
                    
                    AvatarSection(title: "Hair") {
                        ForEach(Avatar.HairType.allCases, id: \.self) { hair in
                            AvatarOption(imageName: hair.rawValue, isSelected: avatar.hair == hair) {
                                avatar.hair = hair
                            }
                        }
                    }
                    
                    AvatarSection(title: "Top") {
                        ForEach(Avatar.TopType.allCases, id: \.self) { top in
                            AvatarOption(imageName: top.rawValue, isSelected: avatar.top == top) {
                                avatar.top = top
                            }
                        }
                    }
                    
                    AvatarSection(title: "Bottom") {
                        ForEach(Avatar.BottomType.allCases, id: \.self) { bottom in
                            AvatarOption(imageName: bottom.rawValue, isSelected: avatar.bottom == bottom) {
                                avatar.bottom = bottom
                            }
                        }
                    }
                    
                    AvatarSection(title: "Face") {
                        ForEach(Avatar.FaceType.allCases, id: \.self) { face in
                            AvatarOption(imageName: face.rawValue, isSelected: avatar.face == face) {
                                avatar.face = face
                            }
                        }
                    }
                }
                Button {
                    profileAvatar = avatar
                    dismiss()
                } label: {
                    Text("Save")
                        .font(Theme.bodyFont)
                }
                .padding()
                .frame(maxWidth: .infinity)
                .background{CardBackground()}
                .padding(.top)
            }
            .padding()
            VStack {
                HStack {
                    BackButton()
                    Spacer()
                }
                .padding()
                Spacer()
            }
        }
    }
}

struct AvatarPreview: View {
    var avatar: Avatar
    
    var body: some View {
        ZStack {
            Image(avatar.body.rawValue).resizable()
            Image(avatar.bottom.rawValue).resizable()
            if avatar.bottom != .dress{
                Image(avatar.top.rawValue).resizable()
            }
            Image(avatar.hair.rawValue).resizable()
            Image(avatar.face.rawValue).resizable()
        }
        .frame(width: 128, height: 128)
        .scaledToFill()
    }
}

struct AvatarSection<Content: View>: View {
    let title: String
    let content: () -> Content
    
    var body: some View {
        VStack(alignment: .leading) {
            Text(title)
                .font(.headline)
                .padding(.leading)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 10) {
                    content()
                }
                .padding(.horizontal)
            }
        }
    }
}

struct AvatarOption: View {
    let imageName: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Image(imageName)
                .resizable()
                .frame(width: 64, height: 64)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(isSelected ? Color.blue : Color.clear, lineWidth: 3)
                )
        }
    }
}

