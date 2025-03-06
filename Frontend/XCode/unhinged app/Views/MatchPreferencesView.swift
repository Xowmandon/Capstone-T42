//
//  MatchPreferencesView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import SwiftUI

enum SexualOrientation : String, CaseIterable, Identifiable {
    case straight = "Straight"
    case gay = "Gay"
    case bisexual = "Bisexual"
    case other = "Other"
    var id : String {self.rawValue}
}

struct MatchPreferencesView: View {
    @EnvironmentObject var appModel : AppModel
    @Environment(\.presentationMode) var presentationMode
    @State private var orientation: SexualOrientation = .straight
    @State private var minAge: Double = 18
    @State private var maxAge: Double = 50
    @State private var preferredGame: String = GameObject.gameList[0].name
    @State private var minHeight: Double = 150
    @State private var location: String = "New York"

    let games : [GameObject] = GameObject.gameList

    var body: some View {
        VStack {
            HStack{
                BackButton()
                Spacer()
            }
            Text("Matching Preferences")
                .font(Theme.titleFont)
                .padding(.bottom, 20)
            VStack {
                HStack {
                    Text("Orientation")
                        .font(Theme.bodyFont)
                    Spacer()
                    Picker("Orientation", selection: $orientation) {
                        ForEach(SexualOrientation.allCases) { orientation in
                            Text(orientation.rawValue).tag(orientation)
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
                            //.font(Theme.bodyFont)
                    }
                    .frame(width: 200)
                    VStack {
                        Slider(value: $maxAge, in: 18...100, step: 1)
                            .accentColor(.blue)
                        Text("Max Age: \(Int(maxAge))")
                            //.font(Theme.bodyFont)
                    }
                    .frame(width: 200)
                }
                .padding()

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
                            //.font(Theme.bodyFont)
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
        .navigationBarBackButtonHidden()
    }
    
    func saveMatchPreferences() {
        print("saveMatchPreferences()")
        //Add settings to preferences struct
        let interestedIn : ProfileGender = MatchPreferencesView.determineInterestFromOrientation(orientation: self.orientation, gender: appModel.profile.gender)
        let interestedInString : String = interestedIn.rawValue
        let preference = MatchPreference(minAge: Int(self.minAge), maxAge: Int(self.maxAge), interestedIn: interestedInString)
            
        //Push preferences to AccountData Singleton
        APIClient.shared.pushPreference(preference: preference)
    }
    
    static func determineInterestFromOrientation(orientation: SexualOrientation, gender: ProfileGender) -> ProfileGender {
        switch(orientation){
        case .other:
            return .other
        case .bisexual:
            return .other
        case .straight:
            return gender == (.male) ? .female : .male
        case .gay:
            return gender == (.male) ? .male : .female
        }
    }
    
}

#Preview{
    MatchPreferencesView()
}
