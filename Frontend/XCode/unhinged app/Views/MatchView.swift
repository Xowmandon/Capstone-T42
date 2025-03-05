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
    
    @State private var offsetX: CGFloat = 0       // For sliding the card horizontally
    @State private var opacity: Double = 1.0     // For fading in and out
    @State private var shouldAnimateProfileCard: Bool = true
    
    private var theme : Theme = Theme.shared // TODO: Add theme settings for profile, change style depending on profile data
    
    var currentProfile: Profile? {
            return appModel.prospectiveMatches.first
    }
    
    //TODO: change values with profile instance
    @ViewBuilder
    func ProfileCard(profile: Profile) -> some View {
        
        ZStack {
            //Profile Image
            VStack (spacing: 0) {
                GeometryReader { geometry in
                    Image(profile.imageName)
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
                        Text("21")
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
    
    var body: some View {
        
        NavigationStack {
            
            ZStack {
                // Profile Content
                ScrollView{
                    
                    Spacer()
                        .frame(minHeight: 80)
                    
                    Text("Let's Match!")
                        .font(Theme.titleFont)
                        .opacity(0.7)
                    
                    //ForEach(appModel.prospectiveMatches.reversed()){ profile in
                    
                    ProfileCard(profile: currentProfile!)
                        .padding(.horizontal)
                        .frame(minHeight: 400)
                    
                    // Basic Info (Attributes?)
                    
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
                    
                    //About Me
                    AboutMeSection(bio: currentProfile?.biography ?? "No bio provided")
                    
                    //TODO: Image Gallery
                    
                    
                    //Prompts
                    
                    ForEach(currentProfile!.prompts ?? []){prompt in
                        PromptView(prompt: prompt)
                            .padding()
                    }
                    //Main buttons spacing
                    Spacer()
                        .padding(.vertical, 60)
                }
                .animation(shouldAnimateProfileCard ? .snappy(duration: 0.5) : nil, value: offsetX) // Slide animation
                .animation(.easeInOut(duration: 0.5), value: opacity) // Fade animation
                .opacity(opacity)
                .offset(x: offsetX)
                
                //Overlay
                VStack {
                    
                    //Navigation Buttons
                    HStack{
                        Button(action: {showAccountConfigSheet.toggle()}){
                            HStack (spacing: 5){
                                
                                //Avatar
                                Circle()
                                Text("\(AccountData.shared.profile.name)")
                                    .font(Theme.bodyFont)
                            }
                            .padding()
                            .background{
                                CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                            }
                        }
                        Spacer()
                        NavigationLink(destination: ConversationsView().navigationTitle("My Matches")){
                            Image("Speech_bubble")
                                .resizable()
                                .scaledToFit()
                                .offset(x:-1, y: 2)
                                .background{
                                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                                }
                        }
                    }
                    .frame(maxHeight: 60)
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
            //refreshMatches()
        }
        
    }
    
    //Reject a Match
    func Pass(){
        
        //Left swipe animation
        withAnimation(){
            offsetX = -UIScreen.main.bounds.width // Slide to the right
            opacity = 0
        }
        
        //Add profile to user's disliked list
        
        //Refresh match prospects
        refreshMatches()
    }
    
    //Accept a Match
    func Match(){
        
        //Right Swipe animation
        withAnimation (Animation.easeIn(duration: 1)) {
            offsetX = UIScreen.main.bounds.width // Slide to the right
            opacity = 0
        }
        
        //add matched profile to matches list
            
        
        //refresh conversations
        //Create conversation with matched profile
            
        //Push changes to DB
        
        //Refresh match prospects
        refreshMatches()
        
    }
    
    func refreshMatches(){
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5){
            
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
        
        //API.getMatches
        appModel.prospectiveMatches.append(AccountData.shared.profile)
        appModel.prospectiveMatches.append(Profile())
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
