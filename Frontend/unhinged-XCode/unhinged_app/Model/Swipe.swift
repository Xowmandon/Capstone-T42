//
//  Swipe.swift
//  unhinged-app
//
//  Created by Joshua Ferguson on 4/21/25.
//

import Foundation

enum SwipeResult: String, Codable {
  case pending  = "PENDING"
  case rejected = "REJECTED"
}

struct Swipe: Codable {
  /// The user who initiated the swipe (optional on send)
  var swiperId: String?

  /// The user being swiped on
  var swipeeId: String

  /// Always send .pending or .rejected
  var swipeResult: SwipeResult

  enum CodingKeys: String, CodingKey {
    case swiperId     = "swiper_id"
    case swipeeId     = "swipee_id"
    case swipeResult  = "swipe_result"
  }
    

}

// 1. Define a response model matching:
//    { "success": "Match created successfully.", "match_id": "XYZ123" }
struct SwipeResponse: Codable {
    let status: String
    let matchId: String?

    enum CodingKeys: String, CodingKey {
        case status
        case matchId = "match_id"
    }
}
