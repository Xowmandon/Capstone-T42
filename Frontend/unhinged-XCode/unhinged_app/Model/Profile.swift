//
//  Profile.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation
import SwiftUI

enum ProfileGender : String, Equatable {
    case male = "male"
    case female = "female"
    case other = "any"
}

class Profile : Identifiable, ObservableObject {
    
    var id : UUID = UUID()
    
    var profile_id : String = "0000"
    
    @Published var name : String
    
    @Published var age : Int = 18
    
    @Published var image : Image = Image("person.fill")
    
    @Published var gender : ProfileGender = .male
    
    @Published var state : USState = .nevada
    
    @Published var city : String = "reno"
    
    //var attributes : [Attribute] = [Attribute(customName: "He/Him", symbolName: "person")]
    
    @Published var biography : String = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    
    var prompts : [PromptItem] = []
    
    var gallery : [ImageGalleryItem]? = []
    
    init(name: String){
        self.name = name
    }
    
    init(id: String = "0000", name: String, age: Int, gender: ProfileGender, state: USState, city: String, bio: String = "No Bio", image: Image = Image(systemName: "person.fill"), galleryItems: [ImageGalleryItem]? = nil) {
        self.profile_id = id
        self.name = name
        self.gender = gender
        self.state = state
        self.city = city
        self.biography = bio
        self.image = image
        self.gallery = galleryItems
    }
    
    func addPrompts(promptList : [PromptItem]){
        self.prompts = promptList
    }
    
    func removePrompt(promptItemIDtoRemove: UUID){
        if let index = prompts.firstIndex(where: { $0.id == promptItemIDtoRemove }) {
            prompts.remove(at: index)
        }
    }
}

enum USState: String, CaseIterable, Identifiable {
    case alabama = "AL"
    case alaska = "AK"
    case arizona = "AZ"
    case arkansas = "AR"
    case california = "CA"
    case colorado = "CO"
    case connecticut = "CT"
    case delaware = "DE"
    case florida = "FL"
    case georgia = "GA"
    case hawaii = "HI"
    case idaho = "ID"
    case illinois = "IL"
    case indiana = "IN"
    case iowa = "IA"
    case kansas = "KS"
    case kentucky = "KY"
    case louisiana = "LA"
    case maine = "ME"
    case maryland = "MD"
    case massachusetts = "MA"
    case michigan = "MI"
    case minnesota = "MN"
    case mississippi = "MS"
    case missouri = "MO"
    case montana = "MT"
    case nebraska = "NE"
    case nevada = "NV"
    case newHampshire = "NH"
    case newJersey = "NJ"
    case newMexico = "NM"
    case newYork = "NY"
    case northCarolina = "NC"
    case northDakota = "ND"
    case ohio = "OH"
    case oklahoma = "OK"
    case oregon = "OR"
    case pennsylvania = "PA"
    case rhodeIsland = "RI"
    case southCarolina = "SC"
    case southDakota = "SD"
    case tennessee = "TN"
    case texas = "TX"
    case utah = "UT"
    case vermont = "VT"
    case virginia = "VA"
    case washington = "WA"
    case westVirginia = "WV"
    case wisconsin = "WI"
    case wyoming = "WY"
    case washingtonDC = "DC"
    
    // Computed property to return the full name of the state
    var fullName: String {
        switch self {
        case .alabama: return "Alabama"
        case .alaska: return "Alaska"
        case .arizona: return "Arizona"
        case .arkansas: return "Arkansas"
        case .california: return "California"
        case .colorado: return "Colorado"
        case .connecticut: return "Connecticut"
        case .delaware: return "Delaware"
        case .florida: return "Florida"
        case .georgia: return "Georgia"
        case .hawaii: return "Hawaii"
        case .idaho: return "Idaho"
        case .illinois: return "Illinois"
        case .indiana: return "Indiana"
        case .iowa: return "Iowa"
        case .kansas: return "Kansas"
        case .kentucky: return "Kentucky"
        case .louisiana: return "Louisiana"
        case .maine: return "Maine"
        case .maryland: return "Maryland"
        case .massachusetts: return "Massachusetts"
        case .michigan: return "Michigan"
        case .minnesota: return "Minnesota"
        case .mississippi: return "Mississippi"
        case .missouri: return "Missouri"
        case .montana: return "Montana"
        case .nebraska: return "Nebraska"
        case .nevada: return "Nevada"
        case .newHampshire: return "New Hampshire"
        case .newJersey: return "New Jersey"
        case .newMexico: return "New Mexico"
        case .newYork: return "New York"
        case .northCarolina: return "North Carolina"
        case .northDakota: return "North Dakota"
        case .ohio: return "Ohio"
        case .oklahoma: return "Oklahoma"
        case .oregon: return "Oregon"
        case .pennsylvania: return "Pennsylvania"
        case .rhodeIsland: return "Rhode Island"
        case .southCarolina: return "South Carolina"
        case .southDakota: return "South Dakota"
        case .tennessee: return "Tennessee"
        case .texas: return "Texas"
        case .utah: return "Utah"
        case .vermont: return "Vermont"
        case .virginia: return "Virginia"
        case .washington: return "Washington"
        case .westVirginia: return "West Virginia"
        case .wisconsin: return "Wisconsin"
        case .wyoming: return "Wyoming"
        case .washingtonDC: return "Washington, D.C."
        }
    }
    
    var id: String { self.rawValue }
}

