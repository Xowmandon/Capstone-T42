//
//  BuildProfileView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI
import PhotosUI

struct BuildProfileView: View {
    
    //TODO: confirm changes upon dismiss
    //TODO: use .overlay for edit button
    
    var profile : Profile = AccountData.shared.getProfile()
    var theme : Theme = Theme.shared
    var editButtonImage : String = "pencil.circle.fill"
    
    @State var showAddObjectSheet : Bool = false
    @State var showAvatarBuilderSheet : Bool = false // TODO: Avatar Builder
    @State var showEditProfileCardSheet : Bool = false // TODO: Image Picker
    @State var showAttributeCreatorSheet : Bool = false  //TODO: Attribute builder
    
    class ImageAttachment: ObservableObject, Identifiable {
        
        /// Statuses that indicate the app's progress in loading a selected photo.
        enum Status {
            /// A status indicating that the app has requested a photo.
            case loading
            
            /// A status indicating that the app has loaded a photo.
            case finished(Image)
            
            /// A status indicating that the photo has failed to load.
            case failed(Error)
            
            /// Determines whether the photo has failed to load.
            var isFailed: Bool {
                return switch self {
                case .failed: true
                default: false
                }
            }
        }
        
        /// An error that indicates why a photo has failed to load.
        enum LoadingError: Error {
            case contentTypeNotSupported
        }
        
        /// A reference to a selected photo in the picker.
        private let pickerItem: PhotosPickerItem
        
        /// A load progress for the photo.
        @Published var imageStatus: Status?
        
        /// A textual description for the photo.
        @Published var imageDescription: String = ""
        
        /// An identifier for the photo.
        nonisolated var id: String {
            pickerItem.identifier
        }
        
        /// Creates an image attachment for the given picker item.
        init(_ pickerItem: PhotosPickerItem) {
            self.pickerItem = pickerItem
        }
        
        /// Loads the photo that the picker item features.
        func loadImage() async {
            guard imageStatus == nil || imageStatus?.isFailed == true else {
                return
            }
            imageStatus = .loading
            do {
                if let data = try await pickerItem.loadTransferable(type: Data.self),
                   let uiImage = UIImage(data: data) {
                    imageStatus = .finished(Image(uiImage: uiImage))
                } else {
                    throw LoadingError.contentTypeNotSupported
                }
            } catch {
                imageStatus = .failed(error)
            }
        }
    }
    
    @State var imageSelection : PhotosPickerItem? {
        
        didSet {
            
            imageSelection!.loadTransferable(type: Image.self) { result in
                
                DispatchQueue.main.async {
                            guard imageSelection == self.imageSelection else { return }
                            switch result {
                            case .success(let image?):
                                // Handle the success case with the image.
                                profileImage = image
                            case .success(nil):
                                // Handle the success case with an empty value.
                                profileImage = Image("person.fill")
                            case .failure(let error):
                                // Handle the failure case with the provided error.
                                print(error)
                            }
                }
                
            }
            
        }
        
    }
    
    /// An array of image attachments for the picker's selected photos.
    //@State var attachment : ImageAttachment
    private var attachmentByIdentifier = [String: ImageAttachment]()
    
    @State var profileImage : Image = Image("person.fill")
    
    @State var name : String
    @State var biography : String
    @State var attributes : [Attribute]
    var prompts : [PromptItem]
    
    @FocusState private var isEditingBiography: Bool
    
    init(){
        //Initialize variables with existing profile data
        _name = State(initialValue: (profile.name))
        _biography = State(initialValue: profile.biography ?? "No Bio written yet")
        _attributes = State(initialValue: profile.attributes)
        prompts = []
    }
    public var body: some View {
        ZStack {
            
            // Profile Content
            ScrollView{
                
                Text("My Profile")
                    .font(Theme.titleFont)
                
                //Avatar Customization
                Text("Avatar")
                    .font(Theme.headerFont)
                Circle()
                    .foregroundStyle(Color.blue)
                    .frame(maxWidth: 100)
                    .overlay{
                        Image(systemName: "pencil.circle.fill")
                            .font(.system(.title))
                            .frame(minWidth: 100, minHeight: 100, alignment: .topTrailing)
                    }
            
                ZStack(alignment: .topTrailing) {
                    ProfileCard(profileImage: profileImage, name: "aa", age: 2)
                        .padding(.horizontal)
                        .frame(minHeight: 400)
                    
                    PhotosPicker(selection: $imageSelection,
                                 matching: .images,
                                 photoLibrary: .shared()) {
                        Image(systemName: "pencil.circle.fill")
                            .symbolRenderingMode(.multicolor)
                            .font(.system(size: 30))
                            .foregroundColor(.accentColor)
                    }
                    .buttonStyle(.borderless)
                     
                }
                
                // Basic Info (Attributes?)
                
                ZStack(alignment:.topTrailing) {
                    VStack (spacing: 5){
                        ForEach(profile.attributes, id: \.self) { attribute in
                            HStack{
                                Image(systemName: attribute.symbolName)
                                Text(attribute.customName)
                                    .font(Theme.bodyFont)
                            }
                        }
                    }
                    .padding()
                    .frame(maxWidth:.infinity)
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    }
                    .padding()
                }
                
                // Biography
                VStack{
                    HStack{
                        Text("About Me!")
                            .font(Theme.headerFont)
                            .padding(.top)
                            .padding(.horizontal)
                        Spacer()
                        
                        Button(action: {
                            isEditingBiography.toggle()
                        }, label: {
                            Image(systemName: editButtonImage).padding(.horizontal).font(.title2)
                        })
                        
                    }
                    TextEditor(text:$biography)
                        .font(Theme.bodyFont)
                        .padding()
                        .focused($isEditingBiography)
                        .toolbar {
                            ToolbarItemGroup(placement: .keyboard) {
                                Spacer()
                                Button("Done") {
                                    isEditingBiography = false // Dismiss keyboard
                                }
                            }
                        }
                }
                .padding()
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                .padding(.horizontal)
                
                //TODO: Image Gallery
                //Prompts
                ForEach(profile.prompts ?? []){prompt in
                    PromptView(prompt: prompt)
                        .padding()
                }
                Spacer()
                    .padding(.vertical, 60)
            }
            
            //Overlay
            VStack {
                HStack{
                    BackButton()
                    Spacer()
                }
                Spacer()
                Button(action: {showAddObjectSheet.toggle()}){
                    Image(systemName: "plus")
                        .imageScale(.large)
                        .symbolRenderingMode(.monochrome)
                        .foregroundStyle(.green)
                        .font(.system(.title, weight: .black))
                        .padding()
                        .background{
                            Circle()
                                .fill(.ultraThickMaterial)
                                .shadow(radius: 5)
                        }
                }
            }
        }
        .navigationBarBackButtonHidden()
        //Add Object Sheet
        .sheet(isPresented: $showAddObjectSheet){
            VStack {
                Text("Customize Your Profile")
                    .font(.headline)
                    .padding()
                VStack {
                    HStack {
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                        Text("Add A Prompt")
                            .padding()
                            .font(.system(.title3, weight: .medium))
                        Spacer()
                    }
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(Color(.secondarySystemBackground))
                        .frame(maxWidth: .infinity, maxHeight: 200)
                        .clipped()
                        .padding(20)
                        .overlay {
                            VStack {
                                Text("What is my favorite food?")
                                    .font(.headline)
                                    .foregroundStyle(.primary)
                                RoundedRectangle(cornerRadius: 10, style: .continuous)
                                    .fill(.orange)
                                    .frame(width: 100, height: 40)
                                    .clipped()
                                    .overlay {
                                        Text("Carrot")
                                    }
                                RoundedRectangle(cornerRadius: 10, style: .continuous)
                                    .fill(.pink)
                                    .frame(width: 100, height: 40)
                                    .clipped()
                                    .overlay {
                                        Text("Cake")
                                    }
                            }
                        }
                }
                VStack {
                    HStack {
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                        Text("Add A Photo")
                            .padding()
                            .font(.system(.title3, weight: .medium))
                        Spacer()
                    }
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(Color(.secondarySystemBackground))
                        .frame(maxWidth: .infinity, maxHeight: 200)
                        .clipped()
                        .padding(20)
                        .overlay {
                            VStack {
                                HStack {
                                    Text("My Favorite Place")
                                        .font(.headline)
                                        .foregroundStyle(.primary)
                                        .padding(.horizontal, 40)
                                    Spacer()
                                }
                                Image("myImage")
                                    .renderingMode(.original)
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .frame(maxWidth: .infinity, maxHeight: 130)
                                    .clipped()
                                    .overlay {
                                        Group {
                                            
                                        }
                                    }
                                    .mask {
                                        RoundedRectangle(cornerRadius: 20, style: .continuous)
                                            .clipped()
                                    }
                            }
                        }
                }
            }
            
        }
        //Profile Card Sheet
        .sheet(isPresented: $showEditProfileCardSheet){
            
        }
    }
    
    func saveProfile() {
        AccountData.shared.setProfile(self.profile)
        
        //TODO: Push new profile data to server
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
    
    BuildProfileView()
    
}
