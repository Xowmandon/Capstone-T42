//
//  KeychainHelper.swift
//  unhinged app
//
//  Created by Harry Sho on 2/27/25.
//

import Foundation
import Security

class KeychainHelper {

    // Save data to the Keychain
    class func save(key: String, value: String) -> Bool {
        guard let data = value.data(using: .utf8) else {
            return false
        }
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key,
            kSecValueData: data
        ]

        // Delete any existing item before saving
        SecItemDelete(query as CFDictionary)

        // Add the new item to the Keychain
        let status = SecItemAdd(query as CFDictionary, nil)
        
        return status == errSecSuccess
    }

    // Retrieve data from the Keychain
    class func load(key: String) -> String? {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key,
            kSecReturnData: kCFBooleanTrue!,
            kSecMatchLimit: kSecMatchLimitOne
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        if status == errSecSuccess {
            if let data = result as? Data, let value = String(data: data, encoding: .utf8) {
                return value
            }
        }
        return nil
    }
    
    ///if let token = KeychainHelper.load(key: "userToken") {
    ///    print("Retrieved token: \(token)")
    ///} else {
    ///    print("No token found.")
    ///}

    // Delete data from the Keychain
    class func delete(key: String) -> Bool {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrAccount: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        return status == errSecSuccess
    }
}
