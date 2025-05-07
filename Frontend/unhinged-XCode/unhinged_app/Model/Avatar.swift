//
//  Avatar.swift
//  unhinged app
//
//  Created by Harry Sho on 3/6/25.
//
// Author: Allison Tang, Harry Aguinaldo

import SwiftUI

struct Avatar: Codable {
    // MARK: – Core traits
    var body: BodyType
    var hair: HairType
    var face: FaceType

    // MARK: – Outfit
    var topCategory: TopCategory
    var topIndex: Int

    var bottomCategory: BottomCategory
    var bottomIndex: Int

    var hatCategory: HatCategory
    var hatIndex: Int

    // MARK: – Nested enums + sprite lists
    enum BodyType: String, CaseIterable, Codable {
        case skin1 = "body_skintone1"
        case skin2 = "body_skintone2"
        case skin3 = "body_skintone3"
        case skin4 = "body_skintone4"
        case skin5 = "body_skintone5"
    }

    enum HairType: String, CaseIterable, Codable {
        case longBlonde = "hair_long_blonde"
        case longBrown  = "hair_long_brown"
        case longBlack  = "hair_long_black"
        case shortBlonde = "hair_short_blonde"
        case shortBrown  = "hair_short_brown"
        case shortBlack  = "hair_short_black"
        case shorterBlonde = "hair_shorter_blonde"
        case shorterBrown  = "hair_shorter_brown"
        case shorterBlack  = "hair_shorter_black"
    }

    enum FaceType: String, CaseIterable, Codable {
        case plain = "face_plain"
        case blush = "face_blush"
    }

    enum TopCategory: String, CaseIterable, Codable {
        case tShirts    = "T-Shirts"
        case hoodies    = "Hoodies"
        case sweatshirts = "Sweatshirts"

        var sprites: [String] {
            switch self {
            case .tShirts:    return (1...7).map { "top_tshirt\($0)" }
            case .hoodies:    return (1...6).map { "top_hoodie\($0)" }
            case .sweatshirts:return (1...6).map { "top_sweatshirt\($0)" }
            }
        }
    }

    enum BottomCategory: String, CaseIterable, Codable {
        case shorts  = "Shorts"
        case pants   = "Pants"
        case dresses = "Dresses"

        var sprites: [String] {
            switch self {
            case .shorts:  return (1...4).map { "bottom_shorts\($0)" }
            case .pants:   return (1...5).map { "bottom_pants\($0)" }
            case .dresses: return (1...3).map { "bottom_dress\($0)" }
            }
        }
    }

    enum HatCategory: String, CaseIterable, Codable {
        case none      = "None"
        case caps      = "Caps"
        case beanies   = "Beanies"
        case headbands = "Headbands"

        var sprites: [String] {
            switch self {
            case .none:      return []
            case .caps:      return (1...3).map { "hat_cap\($0)" }
            case .beanies:   return (1...3).map { "hat_beanie\($0)" }
            case .headbands: return (1...5).map { "hat_headband\($0)" }
            }
        }
    }
}

// ——— AvatarCreator with explicit Top/Bottom sliders ———
struct AvatarCreator: View {
    @Environment(\.dismiss) var dismiss
    @Binding var profileAvatar: Avatar
    @State private var avatar: Avatar

    init(profileAvatar: Binding<Avatar>) {
        self._profileAvatar = profileAvatar
        _avatar = State(initialValue: profileAvatar.wrappedValue)
    }

    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                // Preview
                let topSprite    = avatar.topCategory.sprites[safe: avatar.topIndex] ?? ""
                let bottomSprite = avatar.bottomCategory.sprites[safe: avatar.bottomIndex] ?? ""
                let hatSprite    = avatar.hatCategory.sprites[safe: avatar.hatIndex] ?? ""

                AvatarPreview(
                    avatar: avatar,
                    topSprite:    topSprite,
                    bottomSprite: bottomSprite,
                    hatSprite:    hatSprite
                )
                .padding()

                ScrollView {
                    VStack(spacing: 20) {
                        // Body
                        AvatarSection(title: "Body") {
                            ForEach(Avatar.BodyType.allCases, id: \.self) { body in
                                AvatarOption(
                                    imageName: body.rawValue,
                                    isSelected: avatar.body == body
                                ) { avatar.body = body }
                            }
                        }

                        // Hair
                        AvatarSection(title: "Hair") {
                            ForEach(Avatar.HairType.allCases, id: \.self) { hair in
                                AvatarOption(
                                    imageName: hair.rawValue,
                                    isSelected: avatar.hair == hair
                                ) { avatar.hair = hair }
                            }
                        }

                        // Tops (explicit)
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Top Category")
                                .font(.headline)
                                .padding(.leading)

                            Picker("", selection: $avatar.topCategory) {
                                ForEach(Avatar.TopCategory.allCases, id: \.self) {
                                    Text($0.rawValue).tag($0)
                                }
                            }
                            .pickerStyle(.segmented)
                            .padding(.horizontal)

                            Slider(
                                value: Binding(
                                    get: { Double(avatar.topIndex) },
                                    set: { avatar.topIndex = Int($0) }
                                ),
                                in: 0...Double(avatar.topCategory.sprites.count - 1),
                                step: 1
                            )
                            .padding(.horizontal)

                            Image(avatar.topCategory.sprites[avatar.topIndex])
                                .resizable()
                                .frame(width: 64, height: 64)
                                .padding(.horizontal)
                        }

                        // Bottoms (explicit)
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Bottom Category")
                                .font(.headline)
                                .padding(.leading)

                            Picker("", selection: $avatar.bottomCategory) {
                                ForEach(Avatar.BottomCategory.allCases, id: \.self) {
                                    Text($0.rawValue).tag($0)
                                }
                            }
                            .pickerStyle(.segmented)
                            .padding(.horizontal)

                            Slider(
                                value: Binding(
                                    get: { Double(avatar.bottomIndex) },
                                    set: { avatar.bottomIndex = Int($0) }
                                ),
                                in: 0...Double(avatar.bottomCategory.sprites.count - 1),
                                step: 1
                            )
                            .padding(.horizontal)

                            Image(avatar.bottomCategory.sprites[avatar.bottomIndex])
                                .resizable()
                                .frame(width: 64, height: 64)
                                .padding(.horizontal)
                        }

                        // Hats
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Hat Category")
                                .font(.headline)
                                .padding(.leading)

                            Picker("", selection: $avatar.hatCategory) {
                                ForEach(Avatar.HatCategory.allCases, id: \.self) {
                                    Text($0.rawValue).tag($0)
                                }
                            }
                            .pickerStyle(.segmented)
                            .padding(.horizontal)

                            if avatar.hatCategory != .none {
                                Slider(
                                    value: Binding(
                                        get: { Double(avatar.hatIndex) },
                                        set: { avatar.hatIndex = Int($0) }
                                    ),
                                    in: 0...Double(avatar.hatCategory.sprites.count - 1),
                                    step: 1
                                )
                                .padding(.horizontal)

                                Image(avatar.hatCategory.sprites[avatar.hatIndex])
                                    .resizable()
                                    .frame(width: 64, height: 64)
                                    .padding(.horizontal)
                            }
                        }

                        // Face
                        AvatarSection(title: "Face") {
                            ForEach(Avatar.FaceType.allCases, id: \.self) { face in
                                AvatarOption(
                                    imageName: face.rawValue,
                                    isSelected: avatar.face == face
                                ) { avatar.face = face }
                            }
                        }
                    }
                }

                // Save
                Button {
                    profileAvatar = avatar
                    dismiss()
                } label: {
                    Text("Save")
                        .font(Theme.bodyFont)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background { CardBackground() }
                }
                .padding(.top)
            }
            .padding()

            // BackButton overlay
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

// Helpers

struct AvatarPreview: View {
    var avatar: Avatar
    var topSprite: String
    var bottomSprite: String
    var hatSprite: String

    var body: some View {
        ZStack {
            Image(avatar.body.rawValue).resizable()
            Image(bottomSprite).resizable()
            if !bottomSprite.contains("dress") {
                Image(topSprite).resizable()
            }
            Image(avatar.hair.rawValue).resizable()
            Image(avatar.face.rawValue).resizable()
            if !hatSprite.isEmpty {
                Image(hatSprite).resizable()
            }
        }
        .frame(width: 128, height: 128)
        .scaledToFit()
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
                HStack(spacing: 10) { content() }
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
                        .stroke(isSelected ? .blue : .clear, lineWidth: 3)
                )
        }
    }
}

// Safe-index helper
extension Collection {
    subscript(safe i: Index) -> Element? {
        indices.contains(i) ? self[i] : nil
    }
}
