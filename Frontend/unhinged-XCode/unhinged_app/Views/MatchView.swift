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
    
    //TODO: change values with profile instance
    @ViewBuilder
    func ProfileCard(profile: Profile) -> some View {
        
        ZStack {
            //Profile Image
            VStack (spacing: 0) {
                GeometryReader { geometry in
                    profile.image
                        .resizable()
                        .scaledToFill()
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .mask(Rectangle())
                        .clipped()
                }
                .padding(5)
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                
                //Profile Information
                VStack {
                    HStack(spacing: 20){
                        Text(profile.name)
                            .font(Theme.titleFont)
                            //.font(.system(.largeTitle, weight: .bold))
                            //.offset(x: -2)
                        Spacer()
                        Text(String(profile.age))
                            .font(Theme.titleFont)
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
                        /*
                        RoundedRectangle(cornerRadius: 15)
                            .fill(.red)
                            .shadow(radius:shadowSize)
                            .offset(y:2)
                         */
                    }
                /*
                Image(systemName: "xmark")
                    .imageScale(.large)
                    .symbolRenderingMode(.monochrome)
                    .foregroundStyle(.primary)
                    .font(.system(.title, weight: .black))
                    .foregroundStyle(.pink)
                    .padding()
                    .background{
                        
                        Circle()
                            .fill(.ultraThickMaterial)
                            .shadow(radius:shadowSize)
                    }
                 */
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
                        /*
                        RoundedRectangle(cornerRadius: 15)
                            .fill(.green)
                            .shadow(radius:shadowSize)
                            .offset(y:2)
                         */
                    }
                /*
                Image(systemName: "heart.fill")
                    .imageScale(.large)
                    .symbolRenderingMode(.monochrome)
                    .font(.system(.title, weight: .black))
                    .foregroundStyle(.green)
                    .padding()
                    .background{
                        Circle()
                            .fill(.ultraThickMaterial)
                            .shadow(radius:shadowSize)
                    }
                 */
            }
            .disabled(swipeBufferIsEmpty)
        }
    }
    
    @ViewBuilder
    func AttributeRow(attribute: Attribute) -> some View {
        HStack{
            Image(systemName: attribute.symbolName)
            Text(attribute.customName)
                .font(Theme.bodyFont)
        }
    }
    
    @ViewBuilder
    func AboutMeSection(bio: String) -> some View {
        VStack{
            HStack{
                Text("About Me!")
                    .font(Theme.headerFont)
                    .padding(.top)
                    .padding(.horizontal)
                Spacer()
            }
            Text("\(bio)")
                .font(Theme.bodyFont)
                .padding()
        }
        .padding()
        .background{
            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
        }
        .padding(.horizontal)
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
            NavigationLink(destination: ConversationsView().navigationTitle("My Matches")){
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
                        ProfileCard(profile: currentProfile ?? Profile(name: "NULL PROFILE"))
                            .padding(.horizontal)
                            .frame(minHeight: 400)
                        
                        // Attribute Section
                        
                        /*
                        VStack (spacing: 5){
                            ForEach(currentProfile!.attributes, id: \.self) { attribute in
                                AttributeRow(attribute:attribute)
                            }
                        }
                        .padding()
                        .frame(maxWidth:.infinity)
                        .background{
                            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                        }
                        .padding()
                        */
                        
                        // MARK: Biography Section
                        AboutMeSection(bio: currentProfile?.biography ?? "No bio provided")
                        
                        //TODO: Image Gallery
                        
                        
                        // MARK: Prompts
                        /*
                        if !appModel.prospectiveMatches.first!.prompts.isEmpty {
                            ForEach(appModel.prospectiveMatches.first!.prompts){prompt in
                                PromptView(prompt: prompt)
                                    .padding()
                            }
                        }
                         */
                        
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
        if appModel.prospectiveMatches.isEmpty || appModel.prospectiveMatches.count < 2{
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
