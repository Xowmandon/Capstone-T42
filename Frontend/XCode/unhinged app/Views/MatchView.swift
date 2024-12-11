//
//  MatchView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import SwiftUI
import SwiftData


struct MatchView : View {
    
    @EnvironmentObject var appModel : AppModel
    
    @State private var showAccountConfigSheet : Bool = false
    
    @State private var offsetX: CGFloat = 0       // For sliding the card horizontally
    @State private var opacity: Double = 1.0     // For fading in and out
    @State private var shouldAnimateProfileCard: Bool = true
    
    //TODO: change values with profile instance
    @ViewBuilder
    func ProfileCard(profile: Profile) -> some View {
        
        ZStack {
            
            //Profile Image
            
            GeometryReader { geometry in
                
                Image(profile.imageName)
                    .resizable()
                    .scaledToFill()
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                    .mask(RoundedRectangle(cornerRadius: 20, style: .continuous))
                
            }
            .shadow(radius: 10)
            
            VStack {
                
                Spacer()
                
                //Profile Information
                
                VStack {
                    
                    HStack(spacing: 20){
                    
                        Text(profile.name)
                            .font(.system(.largeTitle, weight: .bold))
                            //.offset(x: -2)
                        Spacer()
                        Text("21")
                            .font(.system(.title))
                        
                        
                    }
                    
                    HStack {
                        Text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia")
                            .frame(maxHeight: 100)
                        Spacer()
                    }
                    
                }
                .foregroundStyle(.white)
                .shadow(radius: 5)
                .padding(.horizontal, 20)
                .padding(.vertical, 30)
                .background{
                    
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .fill(.ultraThinMaterial)
                    
                }
                
                
            }
        }
        
    }
    
    @ViewBuilder
    func AccountConfigSheet() -> some View {
        
        VStack {
            Text("Account Management")
                .font(.system(.title, weight: .semibold))
                .padding(.vertical, 40)
            HStack {
                Text("Logged in as:")
                    .padding(20)
                Spacer()
            }
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(Color(.systemGray6))
                .frame(height: 80)
                .clipped()
                .padding(.horizontal)
                .overlay {
                    HStack {
                        Image("myImage")
                            .renderingMode(.original)
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .mask {
                                Circle()
                                    .padding()
                            }
                            .padding(.trailing)
                        Text("User Name")
                        Spacer()
                        Image(systemName: "apple.logo")
                            .imageScale(.large)
                            .symbolRenderingMode(.monochrome)
                            .padding(.trailing)
                            .font(.title)
                    }
                    .padding(.horizontal, 20)
                }
            Spacer()
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(.blue)
                .frame(height: 80)
                .clipped()
                .padding(.horizontal)
                .overlay {
                    HStack {
                        Text("Log out")
                            .font(.system(.body, weight: .semibold))
                            .foregroundStyle(.white)
                            .padding(.horizontal, 40)
                        Spacer()
                    }
                }
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(.blue)
                .frame(height: 80)
                .clipped()
                .padding(.horizontal)
                .overlay {
                    HStack {
                        Text("Switch User")
                            .font(.system(.body, weight: .semibold))
                            .foregroundStyle(.white)
                            .padding(.horizontal, 40)
                        Spacer()
                    }
                }
            Spacer()
        }
        
        
    }
    
    @ViewBuilder
    func MainButtons() -> some View {
        
        HStack() {
            Spacer()
            
            
            Button {
                
                Pass()
                
            } label: {
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
                    }
            }
            
            Spacer()
            
            Button { OpenProfileDetails() } label: {
                Image(systemName: "heart.text.square.fill")
                    .imageScale(.large)
                    .symbolRenderingMode(.monochrome)
                    .font(.system(.title, weight: .black))
                    .foregroundStyle(.yellow)
                    .padding()
                    .background{
                        
                        Circle()
                            .fill(.ultraThickMaterial)
                        
                    }
            }
            
            Spacer()
            
            Button {
                
                Match()
                
                
            } label: {
                Image(systemName: "heart.fill")
                    .imageScale(.large)
                    .symbolRenderingMode(.monochrome)
                    .font(.system(.title, weight: .black))
                    .foregroundStyle(.green)
                    .padding()
                    .background{
                        
                        
                        Circle()
                            .fill(.ultraThickMaterial)
                        
                    }
            }
            
            Spacer()
            
        }
        .padding()
        .background{
            
            RoundedRectangle(cornerRadius: 20)
                .fill(Color(UIColor.separator))
                .shadow(color: .black.opacity(0.2),radius: 5)
            
        }
        
        
    }
    
    var body: some View {
        
        NavigationStack {
            
            ZStack {
                
                VStack{
                    
                    ZStack{
                    
                        ForEach(appModel.prospectiveMatches.reversed()){ profile in
                            
                            ProfileCard(profile: profile)
                                .padding()
                                .opacity(opacity)
                                .offset(x: offsetX)
                                .animation(shouldAnimateProfileCard ? .snappy(duration: 0.5) : nil, value: offsetX) // Slide animation
                                .animation(.easeInOut(duration: 0.5), value: opacity) // Fade animation
                        }
                            
                            
                    }
                    
                    MainButtons()
                        .padding(.horizontal, 20)
                    
                }
                
            }
            .toolbar{
                /*ToolbarItem(placement: .topBarLeading){
                    
                    Text("Find a Match")
                        .font(.title)
                        .fontWeight(.semibold)
                        
                    
                }*/
                ToolbarItem(placement: .topBarTrailing){
                    
                    
                    Button(action: {showAccountConfigSheet.toggle()}){
                        
                        Image(systemName: "gearshape.fill")
                        
                    }
                    
                }
                ToolbarItem(placement: .topBarTrailing){
                    
                    Button(action: {}){
                        
                        Image(systemName: "person.fill")
                        
                    }
                    
                }
                ToolbarItem(placement: .topBarTrailing){
                    
                    
                    NavigationLink(destination: ConversationsView().navigationTitle("My Matches")){
                        
                        Image(systemName: "message.fill")
                        
                    }
                    
                    /*
                    Button(action: {}){
                        
                        Image(systemName: "message.fill")
                            
                        
                    }
                    */
                   
                }
                
            }
        }
        .sheet(isPresented: $showAccountConfigSheet, onDismiss: didDismissAccountConfigSheet) {
            
            AccountConfigSheet()
            
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
                
                if !appModel.prospectiveMatches.isEmpty{
                 
                    appModel.prospectiveMatches.removeFirst()
                    
                }
                
            }
            
            
        }
        
        
        //API.getMatches
        appModel.prospectiveMatches.append(Profile())
        
        
    }
    
    //Look at possible Match's profile
    func OpenProfileDetails(){
        
        //Get Profile data
        
        //Pass to view
        
        //Push details view onto nav stack
        
    }

    func didDismissAccountConfigSheet(){
        
    }
    
    
}

#Preview {
    NavigationStack{
        MatchView()
            .navigationTitle("Find a Match")
            .environmentObject(AppModel())

    }
}
