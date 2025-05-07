// Author: Benjamin Steinberg
// Created on: 12/11/2024

using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public enum moveType{None, Melee, Magic, Heal, Ultimate}

public class attack : MonoBehaviour
{
    // Public
    public moveType moveType;
    public Image flashImage;

    // Private
    private RPGManager gamemanager;
    private Button button;
    private rpgcharacter currentCharacter;

    void Awake()
    {
        button = GetComponent<Button>();
        if (flashImage != null)
            flashImage.enabled = false;
    }

    public void action()
    {
        gamemanager.receiveAction(moveType);
    }

    public void setGameManager(RPGManager gm)
    {
        gamemanager = gm;
    }

    public void setCharacter(rpgcharacter character)
    {
        currentCharacter = character;
    }

    public void refreshButton()
    {
        if (currentCharacter == null)
        {
            Debug.LogWarning($"[refreshButton] currentCharacter is null for {moveType}");
            return;
        }

        string key = moveType.ToString();
        bool onCooldown = currentCharacter.cooldowns.ContainsKey(key);

        // Enable/disable button
        button.interactable = !onCooldown;

        // Special case for Ultimate flash
        if (moveType == moveType.Ultimate && !onCooldown)
        {
            if (flashImage != null && !flashImage.enabled)
                StartCoroutine(FlashUltimate());
        }
        else if (flashImage != null)
        {
            flashImage.enabled = false;
        }
    }

    private IEnumerator FlashUltimate()
    {
        flashImage.enabled = true;
        Color baseColor = flashImage.color;
        float time = 0f;

        while (currentCharacter != null && !currentCharacter.cooldowns.ContainsKey("Ultimate"))
        {
            time += Time.deltaTime;
            float alpha = Mathf.PingPong(time * 2f, 0.5f) + 0.5f;
            flashImage.color = new Color(baseColor.r, baseColor.g, baseColor.b, alpha);
            yield return null;
        }

        flashImage.enabled = false;
    }

}