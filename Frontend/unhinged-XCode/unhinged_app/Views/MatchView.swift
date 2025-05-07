//
//  MatchView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import SwiftUI

struct MatchView : View {
    
    @EnvironmentObject var appModel : AppModel
    
    @State private var showAccountConfigSheet : Bool = false
    @State private var didCreateNewMatch : Bool = false //TODO: new match banner notification
    @State private var shouldShowProfile : Bool = false
    
    @State private var offsetX: CGFloat = 0       // For sliding the card horizontally
    @State private var opacity: Double = 1.0     // For fading in and out
    @State private var shouldAnimateProfileCard: Bool = true
    
    
    private var theme : Theme = Theme.shared // TODO: Add theme settings for profile, change style depending on profile data
    
    var currentProfile : Profile? {
        guard !swipeBufferIsEmpty else {
            return nil }
        return appModel.prospectiveMatches.first
    }
    var swipeBufferIsEmpty : Bool {
        appModel.prospectiveMatches.isEmpty
    }
    
    
    @ViewBuilder
    func MainButtons() -> some View {
        
        HStack(spacing: 30) {
            Button {
                
                Pass()
                
            } label: {
                Image("X_Button")
                    .padding(5)
                    .background{
                        CardBackground(borderColor: .gray, innerColor: .red)
                            .offset(y:2)
                    }
            }
            .disabled(swipeBufferIsEmpty)
            Button {
                Match()
            } label: {
                Image("Heart")
                    .padding(5)
                    .background{
                        CardBackground(borderColor: .gray, innerColor: .green)
                            .offset(y:2)
                    }
            }
            .disabled(swipeBufferIsEmpty)
        }
    }
    
    //MARK: Body
    var body: some View {
        
        // MARK: Navigation Buttons
        HStack{
            Text("Find a Match")
                .font(Theme.titleFont)
            Spacer()
            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                .overlay{
                    Button(action: {showAccountConfigSheet.toggle()}){
                        Image(systemName:"person.fill")
                            .padding()
                    }
                }
                .frame(maxWidth: 50)
            NavigationLink(destination: ConversationsView().navigationBarBackButtonHidden(true)){
                CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    .overlay{
                        Image("Speech_bubble")
                            .resizable()
                            .scaledToFit()
                            .offset(x:-1, y: 2)
                    }
                    .frame(maxWidth: 50)
            }
        }
        .frame(maxHeight: 50)
        .padding(.horizontal)
        
        NavigationStack {
            
            ZStack {
                // MARK: Profile Content
                ScrollView{
                    if swipeBufferIsEmpty {
                        ProgressView("Getting your Swipes...").foregroundStyle(.primary)
                            .padding(.top, 300)
                            .onAppear{
                                refreshMatches()
                            }
                        Button("Refresh Swipes", systemImage: "arrow.clockwise", action: {
                            refreshMatches()
                        })
                    } else {
                        ProfileContentView(currentProfile: currentProfile)
                    }
                    //Main buttons spacing
                    Spacer()
                        .padding(.vertical, 60)
                }
                .animation(shouldAnimateProfileCard ? .snappy(duration: 0.5) : nil, value: offsetX) // Slide animation
                .animation(.easeInOut(duration: 0.5), value: opacity) // Fade animation
                .opacity(opacity)
                .offset(x: offsetX)
                
                // MARK: Overlay
                VStack {
                    Spacer()
                    MainButtons()
                        .frame(maxWidth: 100)
                }
                .padding()
            }
        }
        .sheet(isPresented: $showAccountConfigSheet){
            AccountConfigSheet()
                .interactiveDismissDisabled(true)
        }
        .onAppear(){
            refreshMatches()
        }
        
    }
    
    func removeTopCardWithAnimation(){
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1){
            
            shouldAnimateProfileCard = false
            
            offsetX = 0
            
            withAnimation (Animation.snappy(duration: 1)) {
                shouldAnimateProfileCard = true
                opacity = 1
                if !appModel.prospectiveMatches.isEmpty {
                    appModel.prospectiveMatches.removeFirst()
                }
            }
        }
    }
    
    //Reject a Match
    func Pass(){
        
        //Left swipe animation
        withAnimation(){
            offsetX = -UIScreen.main.bounds.width // Slide to the right
            opacity = 0
        }
        
        guard let swipedProfile = currentProfile else {
            shouldShowProfile = false
            refreshMatches()
            return
        }
        
        //animate card
        removeTopCardWithAnimation()
        //Add profile to user's disliked list
        Task {
            await APIClient.shared.pushSwipe(swipedUserId: swipedProfile.profile_id, accepted: false)
        }
        //refresh
        refreshMatches()
    }
    
    //Accept a Match
    func Match(){
        
        //Right Swipe animation
        withAnimation (.snappy) {
            offsetX = UIScreen.main.bounds.width // Slide to the right
            opacity = 0
        }
        guard let swipedProfile = currentProfile else {
            shouldShowProfile = false
            refreshMatches()
            return
        }
        removeTopCardWithAnimation()
        
        
        //add matched profile to matches list
        Task {
            let status = await APIClient.shared.pushSwipe(swipedUserId: swipedProfile.profile_id, accepted: true)
            if status == "NEW" {
                didCreateNewMatch = true
            }
        }
        //refresh
        refreshMatches()
        
    }
    
    func refreshMatches() {
        //MARK: Get Swipe Pool
        if appModel.prospectiveMatches.isEmpty || appModel.prospectiveMatches.count == 0{
            shouldShowProfile = false
            Task{
                await appModel.getSwipeProfiles()
            }
            print("Swipe buffer: \(appModel.prospectiveMatches)")
        }
        shouldShowProfile = true
    }

    func didDismissAccountConfigSheet(){
        
    }
    
}

#Preview {
    NavigationStack{
        MatchView()
            .environmentObject(AppModel())

    }
}
