//Author: Benjamin Steinberg
//Date Created: 12/9/24

using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class gridspace : MonoBehaviour
{
    public Button button;
    public SpriteRenderer sprite;
    public TMP_Text letterText;

    private GameController gameCont;
    private int index;

    public void SetGameContrRef(GameController controller, int idx)
    {
        gameCont = controller;
        index = idx;

        if (button == null) button = GetComponent<Button>();
        if (sprite == null) sprite = GetComponentInChildren<SpriteRenderer>();
        if (letterText == null) letterText = GetComponentInChildren<TMP_Text>();

        button.onClick.AddListener(() => gameCont.OnPlayerClickedSpace(index));
    }

    public void SetDisplay(string symbol, Sprite symbolSprite)
    {
        if (letterText != null) letterText.text = symbol;
        if (sprite != null)
        {
            sprite.sprite = symbolSprite;
            sprite.enabled = !string.IsNullOrEmpty(symbol);
        }

        if (button != null)
            button.interactable = string.IsNullOrEmpty(symbol);
    }
}
