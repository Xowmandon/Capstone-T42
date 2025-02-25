//
//  MatchPreferencesView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import SwiftUI

struct MatchPreferencesView: View {
    @Environment(\.presentationMode) var presentationMode
    @State private var orientation: String = "Portrait"
    @State private var minAge: Double = 18
    @State private var maxAge: Double = 50
    @State private var preferredGame: String = ""
    @State private var minHeight: Double = 150
    @State private var location: String = "New York"

    let games : [GameObject] = GameObject.gameList
    let orientations = ["Portrait", "Landscape"]

    var body: some View {
        VStack {
            Text("Matching Preferences")
                .font(Theme.headerFont)
                .padding(.bottom, 20)
            VStack {
                HStack {
                    Text("Orientation")
                        .font(Theme.bodyFont)
                    Spacer()
                    Picker("Orientation", selection: $orientation) {
                        ForEach(orientations, id: \.self) { orientation in
                            Text(orientation).tag(orientation)
                                .font(Theme.bodyFont)
                        }
                    }
                    .pickerStyle(MenuPickerStyle())
                    .frame(width: 150)
                }
                .padding(.bottom, 10)

                HStack {
                    Text("Age Range")
                        .font(Theme.bodyFont)
                    Spacer()
                    VStack {
                        Slider(value: $minAge, in: 18...100, step: 1)
                            .accentColor(.blue)
                        Text("Min Age: \(Int(minAge))")
                            .font(Theme.bodyFont)
                    }
                    .frame(width: 200)
                    VStack {
                        Slider(value: $maxAge, in: 18...100, step: 1)
                            .accentColor(.blue)
                        Text("Max Age: \(Int(maxAge))")
                            .font(Theme.bodyFont)
                    }
                    .frame(width: 200)
                }
                .padding(.bottom, 10)

                HStack {
                    Text("Preferred Game")
                        .font(Theme.bodyFont)
                    Spacer()
                    Picker("Preferred Game", selection: $preferredGame) {
                        ForEach(games, id: \.id) { game in
                            Text(game.name).tag(game.name)
                                .font(Theme.bodyFont)
                        }
                    }
                    .pickerStyle(MenuPickerStyle())
                    .frame(width: 150)
                }
                .padding(.bottom, 10)

                HStack {
                    Text("Minimum Height")
                        .font(Theme.bodyFont)
                    Spacer()
                    VStack {
                        Slider(value: $minHeight, in: 100...250, step: 1)
                            .accentColor(.green)
                        Text("Min Height: \(Int(minHeight)) cm")
                            .font(Theme.bodyFont)
                    }
                    .frame(width: 200)
                }
                .padding(.bottom, 10)

                HStack {
                    Text("Location")
                        .font(Theme.bodyFont)
                    Spacer()
                    TextField("Enter location", text: $location)
                        .font(Theme.bodyFont)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .frame(width: 200)
                }
                .padding(.bottom, 10)

            }
            .padding()
            Button(action: {
                saveMatchPreferences()
                presentationMode.wrappedValue.dismiss()
            } ){
                Text("Save Changes")
                    .font(Theme.bodyFont)
                    .padding()
                    .background{
                        CardBackground()
                    }
                
            }
        }
        .padding()
    }
    
    func saveMatchPreferences() {
        
        
        
        
    }
    
}

#Preview{
    MatchPreferencesView()
}
