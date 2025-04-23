//
//  BuildProfileView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI
import PhotosUI

enum BuildProfileFocusedField: Hashable {
    case none
    case name
    case biography
    case attribute
    case gallery
}

struct BuildProfileView: View {
    
    //TODO: extract subviews
    let isFirstTimeCreation : Bool
    @State var hasMadeChanges : Bool = true
    @State var shouldGoToMatchView : Bool = false
    
    @EnvironmentObject var appModel : AppModel

    @FocusState private var focusedField : BuildProfileFocusedField?
    var editButtonImage : String = "pencil.circle.fill"
    
    @StateObject var profile : Profile
    var theme : Theme = Theme.shared
    
    @State var showAddObjectSheet : Bool = false
    @State var showAvatarBuilderSheet : Bool = false // TODO: Avatar Builder
    
    @State var mainPhoto : Image = Image("default_avatar")
    @State var biographyText : String = ""
    @State var prompts : [PromptItem] = []
    @State var galleryItems : [ImageGalleryItem] = []
    
    
    @State var isShowingExitConfirmation : Bool = false //TODO: exit confirmation
    @State var isShowingDeleteConfirmation: Bool = false
    
    enum DeleteType {
        case prompt
        case gallery
    }
    @State var deleteType : DeleteType?
    @State var promptItemIDToDelete: UUID?
    @State var galleryItemIDToDelete: UUID?
    
    public var body: some View {
        NavigationStack {
            ZStack {
            // MARK: Profile Content
                ScrollView {
                    Text("My Profile")
                        .font(Theme.titleFont)
                    
                    /*
                    //Avatar Customization
                    VStack (alignment: .leading) {
                        Text("Avatar")
                            .font(Theme.headerFont)
                        HStack {
                            Circle()
                                .foregroundStyle(Color.blue)
                                .frame(maxWidth: 100)
                                .overlay{
                                    Image(systemName: "pencil.circle.fill")
                                        .font(.system(.title))
                                        .frame(minWidth: 100, minHeight: 100, alignment: .topTrailing)
                                }
                            VStack{
                                Text("<Select Head>")
                                Text("<Select Top>")
                                Text("<Select Bottom>")
                            }
                        }
                    }
                    */
                    
                    ProfileCard(profileImage: $profile.image, name: $profile.name, age: $profile.age, isEditable: true, focusedField: $focusedField)
                        .frame(minHeight: 400)
                    
                    // Basic Info (Attributes)
                    VStack (spacing : 10){

                        //Location
                        VStack {
                            HStack {
                                Image(systemName: "mappin")
                                    .foregroundStyle(.secondary)
                                Text("Location:")
                                    .font(Theme.headerFont)
                                Spacer()
                            }
                            VStack (alignment: .leading){
                                HStack {
                                    Text("City:")
                                    TextField("City", text: $profile.city)
                                        .focused($focusedField, equals: .attribute)
                                        .background(Color(.quaternarySystemFill))
                                }
                                HStack{
                                    Text("State:")
                                    Picker("Select a State", selection: $profile.state) {
                                        ForEach(USState.allCases) { state in
                                            Text(state.fullName) // Display the full name of the state
                                                .tag(state) // Tag each picker item with the corresponding state
                                        }
                                    }
                                }
                            }
                            .padding(.leading)
                        }
                        .padding()
                        /*
                        ForEach($profile.attributes){ $attribute in
                            VStack (alignment: .leading){
                                Text("Custom Attribute")
                                HStack{
                                    //SF Symbol Picker
                                    Image(systemName: "pencil")
                                        .foregroundStyle(.secondary)
                                    TextField("Name", text: $attribute.customName)
                                        .focused($focusedField, equals: .attributeField)
                                        .background(Color(.quaternarySystemFill))
                                }
                            }
                            .padding()
                        }
                        Spacer()
                         */
                    }
                    .font(Theme.bodyFont)
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    }
                    
                    // Biography
                    VStack{
                        HStack{
                            Image(systemName: "star.fill")
                                .foregroundStyle(.secondary)
                            Text("About Me!")
                                .font(Theme.headerFont)
                            Spacer()
                            Button(action: {
                                focusedField = .biography
                            }, label: {
                                Image(systemName: editButtonImage).padding(.horizontal).font(.title2)
                            })
                            
                        }
                        .padding()
                        
                        TextEditor(text: $biographyText)
                            .focused($focusedField, equals: .biography)
                            .font(Theme.bodyFont)
                            .padding(.horizontal)
                            .padding(.bottom)
                            .onAppear(perform: {biographyText = profile.biography})
                            .frame(minHeight: 150)
                            
                    }
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                        
                    }
                    
                    
                    // MARK: Image gallery
                    
                    ForEach(galleryItems.indices, id: \.self) { index in
                        let photo = galleryItems[index]
                        ZStack(alignment: .topTrailing){
                            ImageGalleryCard(isEditable: false,
                                             galleryItem: $galleryItems[index],
                                             image: photo.image,
                                             title: photo.title,
                                             description: photo.description)
                            Button{
                                
                                galleryItemIDToDelete = galleryItems[index].id
                                deleteType = .gallery
                                isShowingDeleteConfirmation = true
                                                                 
                            } label: {
                                Image(systemName: "trash.fill")
                                    .foregroundStyle(.red)
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                                    .padding()
                            }
                        }
                    }
                    
                    //Prompts
                    ForEach(prompts){ prompt in
                        ZStack (alignment:.topTrailing){
                            PromptView(prompt: prompt)
                            Button{
                                
                                promptItemIDToDelete = prompt.id
                                deleteType = .prompt
                                isShowingDeleteConfirmation = true
                                 
                            } label: {
                                Image(systemName: "trash.fill")
                                    .foregroundStyle(.red)
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                                    .padding()
                            }
                        }
                    }
                    
                    Spacer()
                        .padding(.vertical, 60)
                }
                .padding()
                .confirmationDialog(
                    "Delete this Item?",
                    isPresented: $isShowingDeleteConfirmation,
                    titleVisibility: .visible
                ){
                    Button("Delete", role: .destructive) {
                        DispatchQueue.main.async {
                            switch deleteType {
                            case .prompt:
                                if let id = promptItemIDToDelete {
                                    prompts.removeAll { $0.id == id }
                                }
                                break
                            case .gallery:
                                if let id = galleryItemIDToDelete {
                                    galleryItems.removeAll { $0.id == id }
                                }
                                break
                            case nil:
                                print("Profile Item delete type == NIL ")
                            }
                        }
                    }
                    Button("Cancel", role: .cancel) {}
                } message: {
                   Text("You will not be able to undo this action.")
                }
                
                // MARK: UI Overlay
                VStack {
                    //navbar
                    HStack{
                        if !isFirstTimeCreation {
                            BackButton()
                            Spacer()
                            Button {
                                saveProfile()
                                hasMadeChanges = false
                            } label: {
                                Image(systemName: "checkmark")
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                            }
                        } else {
                            Spacer()
                            Button {
                                isShowingExitConfirmation = true
                                shouldGoToMatchView = true
                            } label: {
                                Image(systemName: "checkmark")
                                    .padding()
                                    .background{
                                        CardBackground()
                                    }
                            }
                            NavigationLink(destination: MatchView().navigationBarBackButtonHidden(), isActive: $shouldGoToMatchView){}
                        }
                    }
                    Spacer()
                    if focusedField == nil || focusedField == .none {
                        Button(action: {showAddObjectSheet.toggle()}){
                            Image(systemName: "plus")
                                .imageScale(.large)
                                .symbolRenderingMode(.monochrome)
                                .foregroundStyle(.green)
                                .font(.system(.title, weight: .black))
                                .padding()
                                .background{
                                    CardBackground()
                                }
                        }
                    }
                }
                .padding()
            }
            .navigationBarBackButtonHidden()
            .toolbar {
                ToolbarItem(placement: .keyboard) {
                    HStack{
                        Spacer()
                        Button() {
                            focusedField = nil // Dismiss keyboard
                        } label: {
                            Image(systemName: "checkmark.circle.fill")
                        }
                    }
                    .fixedSize()
                }
            }
            //Add Object Sheet
            .sheet(isPresented: $showAddObjectSheet){
                AddObjectSheet(prompts: $prompts, galleryItems: $galleryItems)
            }
        }
        .onAppear{
            prompts = appModel.profile.prompts
            mainPhoto = profile.image
        }
        .onDisappear(perform: saveProfile)
    }
    
    func getProfile() {
        
        
    }
    
    func saveProfile() {
        self.profile.biography = biographyText
        
        appModel.profile = self.profile
        //TODO: Push new profile data to server
        Task {
            await APIClient.shared.initProfile(profile: appModel.profile)
        }
        
    }
}


struct AddObjectSheet : View {
    
    @Environment(\.presentationMode) var presentationMode
    
    //@Binding var profile : Profile
    @Binding var prompts : [PromptItem]
    @Binding var galleryItems: [ImageGalleryItem]
    
    @State var dummyGalleryCard : ImageGalleryItem = ImageGalleryItem()
    @State var dummyFocus : BuildProfileFocusedField = .none
    
    var body: some View {
        NavigationStack{
            HStack(spacing: 10){
                BackButton()
                Spacer()
                Text("Customize My Profile")
                    .font(Theme.headerFont)
            }
            .padding()
            List {
                Section {
                    VStack {
                        HStack {
                            Text("Add A Prompt")
                                .font(Theme.headerFont)
                                .padding()
                            
                            NavigationLink(destination: PromptFormView(presentationMode: presentationMode, promptList: $prompts).navigationBarBackButtonHidden()) {}
                        }
                        Text("Keep your matches guessing with a custom prompt - be creative!")
                            .font(Theme.bodyFont)
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                    VStack {
                        PromptView(prompt: PromptItem.examplePrompt)
                            .padding(.horizontal)
                    }
                }
                
                Section{
                    VStack{
                        HStack {
                            Text("Add A Photo")
                                .padding()
                                .font(Theme.headerFont)
                            NavigationLink(destination: CreateGalleryItem(presentationMode: presentationMode, gallery: $galleryItems).navigationBarBackButtonHidden()) {}
                        }
                        Text("Decorate your profile with a photo.")
                    }
                    ImageGalleryCard(isEditable: false, galleryItem: $dummyGalleryCard)
                }
            }
        }
    }
}

private extension PhotosPickerItem {
    var identifier: String {
        guard let identifier = itemIdentifier else {
            fatalError("The photos picker lacks a photo library.")
        }
        return identifier
    }
}

#Preview{
    
    BuildProfileView(isFirstTimeCreation: false,profile: Profile())
        .environmentObject(AppModel())
    
}
