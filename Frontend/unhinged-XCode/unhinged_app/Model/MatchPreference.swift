//
//  MatchPreference.swift
//  unhinged app
//
//  Created by Harry Sho on 3/6/25.
//

struct MatchPreference : Codable {
    
    var minAge: Int = 18
    var maxAge: Int = 50
    var interestedIn: String = ""
    //var city: String = ""
    //var state: String = USState.nevada.rawValue
    //var preferredGame: String = GameObject.gameList[0].name
    //var minHeight: Double = 150
}
