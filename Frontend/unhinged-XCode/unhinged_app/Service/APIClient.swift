//
//  APIClient.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//  Pair Programmed With Joshua Ferguson (Xowmandon)
//

import Foundation
import Alamofire
import AlamofireImage
import SwiftUI
import UIKit

class APIClient {
    
    static let shared = APIClient()
    let imageCache = AutoPurgingImageCache()
    private init() {}
    
    enum TaskType {
        case get
        case post
        case postForm
    }
    enum TaskError : Error{
        case failedToSaveToken
        case invalidValue(String)
    }
    
    func apiTask(
        type: TaskType,
        endpoint: String,
        hasHeader: Bool,
        headerValue: String? = "",
        headerField: String? = "",
        queryItems: [URLQueryItem]? = nil,
        payload: Data?
    ) async throws -> Data {
        
        var urlComponents = URLComponents(string: "https://cowbird-expert-exactly.ngrok-free.app/\(endpoint)")!
        urlComponents.queryItems = queryItems ?? []
        
        guard let url = urlComponents.url else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = type == .get ? "GET" : "POST"
        
        if hasHeader {
            request.setValue(headerValue ?? "", forHTTPHeaderField: headerField ?? "")
        }
        
        switch type {
        case .post:
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = payload
        case .postForm:
            request.httpMethod = "POST"
            request.setValue("multipart/form-data", forHTTPHeaderField: "Content-Type")
            request.httpBody = payload
        default:
            break
        }

        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw URLError(.badServerResponse)
        }
        
        return data
    }
    
    // MARK: send identity token
    struct IdentityTokenResponse : Codable {
        let message : String
        let token : String
    }
    func sendIdentityToken(token: String) async {
        print("Sending identity token")
        let body : [String : String] = ["auth_method": "apple",
                                        "identity_token": token]
        guard let payload = try? JSONEncoder().encode(body) else {
            print("failed to encode payload")
            return
        }
        do {
            let data = try await apiTask(type: .post, endpoint: "signup", hasHeader: false, payload: payload)
            let tokenResponse : IdentityTokenResponse = try JSONDecoder().decode(IdentityTokenResponse.self, from: data)

            let success = KeychainHelper.save(key: "JWTToken", value: tokenResponse.token)
            if success {
                print("Successfully saved token")
                try await self.verifyJWTToken()
            } else {
                print("Failed to save token")
            }
            
        } catch {
            print("Failed to receive Token: \(error.localizedDescription)")
        }

    }
    
    // MARK: Verify JWT Token
    func verifyJWTToken() async throws {
        let token : String = KeychainHelper.load(key: "JWTToken")!
        print(token as String)
        do {
            let data = try await apiTask(type: .get, endpoint: "verify_token", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Verify Token Failed: \(error)")
        }
        print("Verified Token Success")
    }
    
    // MARK: Push Profile
    func initProfile(profile: Profile) async {
        print("init Profile")
        let token : String = KeychainHelper.load(key: "JWTToken")!
        let profileData : [String:String] = ["age":"\(profile.age)",
                                             "name":profile.name,
                                             "gender":"\(profile.gender.rawValue)",
                                             "state":"\(profile.state.rawValue)",
                                             "city":profile.city,
                                             "bio":profile.biography]
        guard let payload = try? JSONEncoder().encode(profileData) else {
            fatalError("Failed to encode payload")
        }
        print("INIT PROFILE PAYLOAD: \(payload)")
        do {
            let data = try await apiTask(type: .post, endpoint: "users/profile", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: payload)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Failed to init profile: \(error.localizedDescription)")
        }
    }
    
    // MARK: Push Preferences
    func pushPreference(preference: MatchPreference) async {
        print("attempting to push preference")
        let token : String = KeychainHelper.load(key: "JWTToken")!
        let preferenceData : [String:String]  = ["minAge":"\(preference.minAge)",
                                                 "maxAge":"\(preference.maxAge)",
                                                 "interestedIn":"\(preference.interestedIn)"]
        guard let payload = try? JSONEncoder().encode(preferenceData) else {
            fatalError("Failed to encode payload")
        }
        
        let urlQueryItems = [URLQueryItem(name: "limit", value: "20")]
        
        do {
            let data = try await apiTask(type: .post, endpoint: "users/preferences", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", queryItems: urlQueryItems, payload: payload)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Push Preference failed: \(error.localizedDescription)")
        }
        
    }
    
    // MARK: Decode Profile
    // Get Swipe profiles for MatchView()
    func decodeProfile (person: [String:String]) async throws -> Profile  {
        
        //get attributes
        guard let idString  = person["userID"] else {
            throw TaskError.invalidValue("idstring")
        }
        
        guard let ageString    = person["age"] else {
            throw TaskError.invalidValue("agestring")
        }
        let age: Int?    = Int(ageString)
        
        guard let name   = person["name"] else {
            throw TaskError.invalidValue("nameString")
        }
        
        guard let genderString = person["gender"] else {
            throw TaskError.invalidValue("genderString")
        }
        guard let gender = ProfileGender(rawValue: genderString) else{
            print("Failed to match ProfileGender case: \(genderString)")
            throw TaskError.invalidValue("\(genderString)")
        }
        
        let stateString  = person["state"]
        guard let stateCode = USState(rawValue: stateString ?? "") else {
            print("Failed to match USState case: \(String(describing: stateString))")
            throw TaskError.invalidValue("stateCode")
        }
        
        guard let cityString: String   = person ["city"] else {
            print("invalid city string")
            throw TaskError.invalidValue("cityString")
        }
        guard let bioString: String    = person["bio"] else {
            print("invalid bio string")
            throw TaskError.invalidValue("bioString")
        }
        
        //get photos
        var mainPhoto : SwiftUI.Image = SwiftUI.Image(systemName: "person.fill")
        var galleryItems : [ImageGalleryItem] = []
        
        let imgs = await getProfileImgs(userId: idString)
        print("GET IMGS RETURNED: \(imgs)")
        
        if let mainPhotoList = imgs["main_photo"], !mainPhotoList.isEmpty,
           let mainPhotoURL = mainPhotoList.first,  // Safely get first element
           let url = URL(string: mainPhotoURL) {    // Safely create URL
            
            if let cachedImage = self.imageCache.image(for: URLRequest(url: url),
                                          withIdentifier: mainPhotoURL) {
                mainPhoto = Image(uiImage: cachedImage)
                print("DECODE PROFILE MAIN PHOTO: \(mainPhotoURL)")
            } else {
                print("DECODE PROFILE MAIN PHOTO: FOUND BUT NOT CACHED - \(mainPhotoURL)")
            }
        } else {
            print("DECODE PROFILE MAIN PHOTO: NONE")
        }
        
        if let userPhotoUrls = imgs["user_photos"],
           let galleryItemTitles = imgs["titles"],
           let galleryItemDescs = imgs["descriptions"] {
            for (url, (title, desc)) in zip(userPhotoUrls, zip(galleryItemTitles, galleryItemDescs)) {
                print("DECODE USER PHOTO: \(url)")
                let galleryPhotoUIImage = self.imageCache.image(for: URLRequest(url: URL(string: url)!),withIdentifier: url) //may need URLRequest
                let galleryImg = Image(uiImage: galleryPhotoUIImage!)
                galleryItems.append(ImageGalleryItem(image: galleryImg, title: title, description: desc))
            }
        } else {
            print("DECODE PROFILE USER PHOTOS: NONE")
        }
    
        return Profile(id: idString, name: name, age: age ?? -1, gender: gender, state: stateCode, city: cityString, bio: bioString, image: mainPhoto, galleryItems: galleryItems,)
    }
    
    //MARK: Get Swipes
    func getSwipes (limit: Int) async -> [Profile] {
        print("Attempting to pull swipe pool")
        let queryLimit : [URLQueryItem] = [URLQueryItem(name: "limit", value: String(limit))]
        let token : String = KeychainHelper.load(key: "JWTToken")!
        var profiles : [Profile] = []
        do {
            let data = try await apiTask(type: .get, endpoint: "users/swipe_pool", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", queryItems: queryLimit, payload: nil)
            print(data as Any)
            let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
            print(response)
            for person in response {
                print("decoding \(person)")
                let personProfile = try await self.decodeProfile(person: person)
                
                /*
                let decodedName = personProfile.name
                print("decodedName: \(decodedName)")
                let decodedID = personProfile.profile_id
                print("decodedID : \(decodedID)")
                */
                profiles.append(personProfile)
            }
        } catch {
            print("getSwipes failed with error: \(error.localizedDescription)")
        }
        
        print("pulled profiles: \(String(describing: profiles))")
        
        return profiles
    }
    
    //Get Matches for ConversationsView()
    /*
    struct getMatchesResponse : Decodable {
        let id : String
        let matchedUserId : String
        let matchedName : String
        let matchDate : String
        let lastMessage : String
        let profile : [String:String]
    }
     */
    
    // MARK: Get Matches (Conversations)
    func getMatches () async -> [Conversation] {
        
        var pulledConversations : [Conversation] = []
        let token : String = KeychainHelper.load(key: "JWTToken")!
        
        print("Attempting to pull matches")
        do {
            let data = try await apiTask(type: .get, endpoint: "users/matches", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil)
            let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
            print(response)
            for match in response {
                print ("GOT MATCH: \(match)")
                
                guard   let id = match["match_id"],
                        let matchedUserId = match["matched_user_id"],
                        let matchedName = match["matched_user_name"],
                        let matchDate = match["match_date"],
                        let lastMessage = match["last_message"] else {
                    
                    throw NSError(domain: "Failed to decode", code: 1000, userInfo: nil)
                }
                guard let matchedProfile : Profile = await getProfile(userID: matchedUserId) else {
                    throw NSError(domain: "No profile exists", code: 1000, userInfo: nil)
                }
                let conversation = Conversation(matchId: id,
                                                matchedUserId: matchedUserId,
                                                matchedName: matchedName,
                                                matchDate: matchDate,
                                                lastMessage: lastMessage,
                                                matchedProfile: matchedProfile)
                
                pulledConversations.append(conversation)
            }
            
        } catch {
            print("getMatches failed with error: \(error.localizedDescription)")
        }
        return pulledConversations
    }
    // MARK: Get message
    //Get messages associated with a match (Conversation)
    func getConversationMessages (match_id: String, limit: Int?, page: Int?, all_messages: Bool?) async -> [Message] {
        // Author: Joshua Ferguson (Xowmandon)
        var pulledMessages : [Message] = []
        
        print("Attmepting to pull messages for match_id: \(match_id)")
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return pulledMessages
        }
        // URL Parameters
        var queryItems = [ URLQueryItem(name: "match_id", value: match_id) ]
        
        if let limitOpt = limit {
            queryItems.append(URLQueryItem(name: "limit", value: String(limitOpt)))
        }
        if let pageOpt = page {
            queryItems.append(URLQueryItem(name: "page", value: String(pageOpt)))
        }
        
        if let all_messages_opt = all_messages {
            queryItems.append(URLQueryItem(name: "all_messages", value: String(all_messages_opt)))
        }
        
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "users/messages/conversation",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            let decoder = JSONDecoder()
            let resp = try decoder.decode(MessageResponse.self, from: data)
            let messages = resp.messages
            pulledMessages = messages
            print("Total \(messages.count) messages for match \(resp.matchId)")
        }
        catch {
            print("⚠️ Get Messages failed:", error)
        }
        return pulledMessages
    }
        
    // MARK: Push Message
    //Send message to conversation associated with match
    func pushConversationMessage (match_id: String, msgType: Message.Kind?, content: String) async {
        // Author: Joshua Ferguson (Xowmandon)

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        var payload: [String: String] = ["match_id" : match_id,
                                         "kind"     : "",
                                         "message_content": content,]
        // if you ever want to send kind to server:
        if let kind = msgType {
            payload["kind"] = kind.rawValue
        }

        // 3️⃣ Serialize to Data
        guard let body = try? JSONSerialization.data(withJSONObject: payload, options: []) else {
            print("❌ Failed to serialize JSON payload")
            return
        }

        do {
            let _ = try await apiTask(
                type: .post,
                endpoint: "users/messages",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: nil,
                payload: body
            )
            print("✅ Message sent successfully: \(body)")
        } catch {
            print("❌ pushConversationMessage failed:", error.localizedDescription)
        }
    }

    //MARK: Push Swipe
    func pushSwipe(swipedUserId: String, accepted: Bool) async -> String? {
        // Author: Joshua Ferguson (Xowmandon), pair programmed with Harry Aguinaldo

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return nil
        }
        
        let result: SwipeResult = accepted ? SwipeResult.pending : SwipeResult.rejected
        let swipe = Swipe(
            swiperId:    nil,
            swipeeId:    swipedUserId,
            swipeResult: result,
        )
        
        let encoder = JSONEncoder()
        let decoder = JSONDecoder()
        
        // Make POST Request, with JWT TOken
        do {
            let body = try encoder.encode(swipe)
            let data = try await apiTask(
                type: TaskType.post,
                endpoint: "users/swipes",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                payload: body
            )
            
            do {
                // Check for New Match Object
                let resp = try decoder.decode(SwipeResponse.self, from: data)
                //print("✅ \(resp["status"])")
                if let matchId = resp.matchId {
                    // 🎉 New match! handle it here
                    print("🎉 New match detected! match_id = \(matchId)")
                    return resp.status
                    // e.g. navigate to chat screen, notify UI, etc.
                } else {
                    // ✅ Swipe went through, but no match yet
                    print("✅ Swipe sent successfully. No match detected.")
                }
                
            } catch {
                print("⚠️ Could not parse response:", error)
            }
        } catch {
            print("❌ failed to encode Swipe payload:", error)
        }
        
        return ""
    }
    
    
    // MARK: Poll Matches
    func pollMatches() async -> Bool {
        // Author: Joshua Ferguson (Xowmandon)
        
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return false
        }

        // Poll for new matches
        // Make GET Request, with JWT Token
        let decoder = JSONDecoder()
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "poll/matches",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: nil,
                payload: nil
            )
    
            let resp = try decoder.decode(PollMatchesResponse.self, from: data)
            if resp.status == "NEW" {
                print("🎉 New match detected!")
                return true
                // Handle new match here (TODO)
                // Resp Structure:
                // {
                //     "status": "NEW",
                //     "match_id": "12345",
                //     "matched_user_id": "67890",
                //     "matched_user_name": "John Doe",
                //     "match_date": "2023-10-01T12:00:00Z",
                //     "last_message": "Hello!"
                // }
                
            } else {
                print("No new matches.")
            }
        } catch {
            print("⚠️ Could not parse response:", error.localizedDescription)
        }
        // Send Signal if Returns New Match
        return false
    }
    
    // MARK: Poll messages
    func pollMessages(matchId: String? = nil) async -> Bool {
        // Author: Joshua Ferguson (Xowmandon)

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return false
        }

        print("Attempting to poll messages...Match ID: \(matchId ?? "No Match ID")")

        // If matchId is nil, then poll all messages
        // If matchId is not nil, then poll messages for that matchId
        let queryItems = matchId != nil ? [URLQueryItem(name: "match_id", value: matchId)] : nil

        let decoder = JSONDecoder()
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "poll/messages",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            let resp = try decoder.decode(PollMessagesResponse.self, from: data)
            if resp.status == "NEW" {
                
                // Sanity & Validation Print
                print("🎉 New messages detected for match_id: \(resp.matchId ?? "")")
                print("Messages: \(resp.messages)")
                print("Total messages: \(resp.messages.count)")
                return true
                
                // Handle new messages here (TODO)
                // Resp Structure:
                // {
                //     "status": "NEW",
                //     "match_id": "12345",
                //     "messages": [
                //         {
                //             "message_id": "1",
                //             "content": "Hello!",
                //             "sentFromClient": true,
                //             ...
                //         },
                //         ...
                //     ]
                // }
                
            } else {
                print("No new messages Found.")
            }
        } catch {
            print("⚠️ Could not parse response:", error.localizedDescription)
        }
        return false
    }
    
    
    // MARK: Get profile
    func getProfile(userID: String?) async -> Profile? {
        var profile: Profile?
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return nil
        }

        var queryItems : [URLQueryItem] = []
        
        if let userID {
            queryItems.append(URLQueryItem(name: "user_id", value: userID))
        }
        
        do {
            let data = try await apiTask(type: .get,
                                         endpoint: "users/profile",
                                         hasHeader: true,
                                         headerValue: "Bearer \(token)",
                                         headerField: "X-Authorization",
                                         queryItems: queryItems,
                                         payload: nil)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
            profile = try await decodeProfile(person: response)
            print("Got profile: \(String(describing: profile?.name))")
        } catch {
            print("Get Profile failed with error \(error.localizedDescription)")
        }
        return profile
    }
    
    // MARK: Get Images (Main, Gallery)
    struct ImgResponse : Codable {
        
        var main_photo : String
        var user_photos : [String]
        var titles : [String]
        var descriptions : [String]
        
        init(from decoder: Decoder) throws {
            let container = try decoder.container(keyedBy: CodingKeys.self)

            // Decode each field with fallback defaults
            self.main_photo = (try? container.decode(String.self, forKey: .main_photo)) ?? ""
            self.user_photos = (try? container.decode([String].self, forKey: .user_photos)) ?? []
            self.titles = (try? container.decode([String].self, forKey: .titles)) ?? []
            self.descriptions = (try? container.decode([String].self, forKey: .descriptions)) ?? []
        }
        
    }
    private func getProfileImgs(userId: String? = nil) async -> [String: [String]] {
        // Initialize empty results
        var result: [String: [String]] = [
            "main_photo": [],
            "user_photos": [],
            "titles": [],
            "descriptions": []
        ]
        
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return result
        }
        
        print("📥 Fetching profile images...")
        
        // If userId is nil, then Fetch Current User's Profile Images
        let queryItems: [URLQueryItem]? = userId != nil ? [URLQueryItem(name: "user_id", value: userId)] : nil
        
        do {
            // Make GET Request for Main and Additional Profile Picture S3 URLS
            let data = try await apiTask(
                type: .get,
                endpoint: "users/profile_picture",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            
            print("✅ getProfileImgs Success")
            let decoder = JSONDecoder()
            let resp = try decoder.decode(ImgResponse.self, from: data)
            print("GET PROFILE IMG RESPONSE: \(resp)")
            
            // Process main photo
            let mainPhotoURL = resp.main_photo
            result["main_photo"] = [mainPhotoURL]
            await cacheImage(urlString: mainPhotoURL)
            
            // Process user photos
            let userPhotos = resp.user_photos
            let titles = resp.titles
            let descriptions = resp.descriptions
                
            result["user_photos"] = userPhotos
            result["titles"] = titles
            result["descriptions"] = descriptions
            
            // Cache all user photos
            await withTaskGroup(of: Void.self) { group in
                for urlString in userPhotos {
                    group.addTask {
                        await self.cacheImage(urlString: urlString)
                    }
                }
            }
            
        } catch {
            print("⚠️ Get Profile Imgs failed with error:", error)
        }
        
        print("GOT PROFILE IMG DATA: \(result)")
        return result
    }

    private func cacheImage(urlString: String) async {
        guard let url = URL(string: urlString) else { return }
        
        return await withCheckedContinuation { continuation in
            AF.request(url).responseImage { response in
                switch response.result {
                case .success(let image):
                    let request = URLRequest(url: url)
                    self.imageCache.add(image, for: request, withIdentifier: urlString)
                    print("✅ Cached image: \(urlString)")
                    let requested = URLRequest(url: URL(string: urlString)!)
                    guard let _ = self.imageCache.image(for: requested, withIdentifier: urlString) else {
                        print("Failed to Retrieve Cached Image: <\(urlString)> <\(requested)>")
                        return
                    }
                case .failure(let error):
                    print("❌ Failed to fetch image \(urlString):", error.localizedDescription)
                }
                continuation.resume()
            }
        }
    }
    
    // MARK: Prompts
    
    func getPrompts() async -> [PromptItem] {
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return []
        }
        
        return []
    }
    
    /*
    private func getProfileImgs(userId: String? = nil) async -> [String:[String]] {
        
        var mainPhotoURL : [String] = []
        var userPhotoURLs : [String] = []
        
        var userPhotoTitles : [String] = []
        var userPhotoDescs : [String] = []
        
        // Author: Joshua Ferguson (Xowmandon), harry
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return [:]
        }
        print("📥 Fetching profile images...")

        // If userId is nil, then Fetch Current User's Profile Images
        let queryItems: [URLQueryItem]? = userId != nil ? [URLQueryItem(name: "user_id", value: userId)] : nil

        // Make GET Request for Main and Additional Profile Picture S3 URLS
        let data : Data
        let resp : ImgResponse = ImgResponse()
        do {
            data = try await self.apiTask(
                type: .get,
                endpoint: "users/profile_picture",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            print("✅ getProfileImgs Success")
            let decoder = JSONDecoder()
            let resp = try decoder.decode(ImgResponse.self, from: data)
            print("GET PROFILE IMG RESPONSE: \(resp)")
            
        } catch {
            print("⚠️ Get Profile Imgs failed with error:", error)
        }
        
        await Task {
            // Decode Main Photo
            //var pulledProfileImageURLReqs : [URLRequest] = []
            if let pfpImgURLString = resp.main_photo,
               let pfpImgURL = URL(string: pfpImgURLString) {
                let pfpImgURLRequest = URLRequest(url: pfpImgURL)
                mainPhotoURL.append(pfpImgURLString)
                AF.request(pfpImgURLRequest).responseImage { response in
                    print("AF MAIN PHOTO REQUEST: \(response)")
                    switch response.result {
                    case .success(let image):
                        self.imageCache.add(image, for: pfpImgURLRequest, withIdentifier: pfpImgURLString)
                        print("✅ Cached image: \(pfpImgURL)")
                    case .failure(let error):
                        print("❌ Failed to fetch image:", error.localizedDescription)
                    }
                }
                
            }
            // Decode Additional Photos
            var pulledGalleryImageURLReqs : [URLRequest] = []
            if let pulledGallery = resp.user_photos,
               let pulledTitles = resp.titles,
               let pulledDescs = resp.descriptions
            {
                userPhotoURLs = pulledGallery
                userPhotoTitles = pulledTitles
                userPhotoDescs = pulledDescs
                
                for urlString in pulledGallery {
                    if let url = URL(string: urlString){
                        let galleryItemRequest = URLRequest(url: url)
                        pulledGalleryImageURLReqs.append(galleryItemRequest)
                    }
                }
                for (urlString, urlReq) in zip(pulledGallery, pulledGalleryImageURLReqs) {
                    AF.request(urlReq).responseImage { response in
                        print("AF USER PHOTO REQUEST: \(response)")
                        switch response.result {
                            case .success(let image):
                            self.imageCache.add(image, for: urlReq, withIdentifier: urlString)
                                print("✅ Cached image: \(urlString)")
                            case .failure(let error):
                                print("❌ Failed to fetch image:", error.localizedDescription)
                            }
                    }
                }
                
            } else {
                print("NO USER IMAGES FOUND")
            }
            
        }

        
        let profileImgData = ["main_photo" : mainPhotoURL,
                              "user_photos" : userPhotoURLs,
                              "titles" : userPhotoTitles,
                              "descriptions" : userPhotoDescs]
        
        print("GOT PROFILE IMG DATA: \(profileImgData)")
        
        return profileImgData
        
    }
    */
    // MARK: Push Profile Image
    func pushProfileImg(isMainPhoto : Bool, title : String?, description: String?, image: SwiftUI.Image) async {
        //Author: Joshua Ferguson, pair programmed with Harry Aguinaldo
        
        let uiImage = imageToUIImage(image: image, size: CGSize(width: 400, height: 400))
        
        // Make POST Request with JWT Token
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found in Keychain")
            return
        }

        // UIImage to JPEG Data Validation
        guard let imageData = uiImage.jpegData(compressionQuality: 0.8) else {
            print("❌ Failed to convert UIImage to JPEG data")
            return
        }
        
        print("📤 Preparing to upload profile image...")

        // Request Params and Headers
        let endpoint = "https://cowbird-expert-exactly.ngrok-free.app/users/profile_picture"
        let fileName = "\(UUID().uuidString).jpg"
        let headers: HTTPHeaders = [
            "Content-Type": "multipart/form-data",
            "X-Authorization": "Bearer \(token)"
        ]

        // Alamofire Upload Request Form
        AF.upload(multipartFormData: { multipartFormData in

            // Image Data Form Data
            multipartFormData.append(
                imageData,
                withName: "profile_picture",
                fileName: fileName,
                mimeType: "image/jpeg"
            )

            // is_main_photo Form Data
            multipartFormData.append(Data("\(isMainPhoto)".utf8), withName: "is_main_photo")
            if !isMainPhoto {
                multipartFormData.append(Data("\(title!)".utf8), withName: "title")
                multipartFormData.append(Data("\(description!)".utf8), withName: "description")
            }

        }, to: endpoint, method: .post, headers: headers)
        .validate(statusCode: 200..<300)
        .response { response in
            if let error = response.error {
                print("❌ Upload failed:", error.localizedDescription)
                return
            }

            // Validate Data Recieved
            guard let data = response.data else {
                print("❌ No response data received")
                return
            }

            // Decode Data
            do {
                if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ Image uploaded successfully. Server response:", json)
                    if let imageUrl = json["url"] as? String,
                    let url = URL(string: imageUrl) {
                        print("🔗 Image URL: \(url)")
                    } else {
                        print("❌ Invalid or missing image URL in response")
                    }
                } else {
                    print("⚠️ Response is not in expected JSON format")
                }
            } catch {
                print("⚠️ Failed to parse JSON response:", error)
            }
        }
    }
    func imageToUIImage(image: SwiftUI.Image, size: CGSize) -> UIImage {
        DispatchQueue.main.sync{
            let controller = UIHostingController(rootView: image
                .resizable()
                .aspectRatio(contentMode: .fill)
                //.offset(y: -20)
                .frame(width: size.width, height: size.height)
                .ignoresSafeArea()
            )

            let view = controller.view
            let targetSize = CGSize(width: size.width, height: size.height)

            let window = UIWindow(frame: CGRect(origin: .zero, size: targetSize))
            window.rootViewController = controller
            window.makeKeyAndVisible()

            view?.bounds = window.bounds
            view?.backgroundColor = .clear
            view?.layoutIfNeeded()

            let renderer = UIGraphicsImageRenderer(size: targetSize)
            return renderer.image { _ in
                view?.drawHierarchy(in: view!.bounds, afterScreenUpdates: true)
            }
        }
    }

}



struct PollMatchesResponse: Codable {
    let status: String
    let matchId: String?
    let matchedUserId: String?
    let matchedUserName: String?
    let matchDate: String?
    let lastMessage: String?

    enum CodingKeys: String, CodingKey {
        case status
        case matchId = "match_id"
        case matchedUserId = "matched_user_id"
        case matchedUserName = "matched_user_name"
        case matchDate = "match_date"
        case lastMessage = "last_message"
    }

}


struct PollMessagesResponse: Codable {
    let status: String
    let matchId: String?
    let messages: [Message]

    enum CodingKeys: String, CodingKey {
        case status = "status"
        case matchId = "match_id"
        case messages = "messages"
    }
}
