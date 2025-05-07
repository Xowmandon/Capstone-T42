//Author: Benjamin Steinberg
//Created on: 12/10/2024
using System;
using System.Collections.Generic;
using UnityEngine;

public enum BossType {
    Ricardio,
    TheAlgorithm,
    LovebombTed
}

[System.Serializable]
public struct BossStats {
    public string name;
    public string meleeName;
    public string magicName;
    public string AOEName;
    public string ultimateName;
    public bool appliesBurn;
    public bool healsAfterAction;
    public float aoeChance;
    public Sprite sprite;
    public Vector3 position;
    public Vector3 scale;
    public float maxHealth;
    public float meleeDamage;
    public float magicDamage;
    public float ultimateDamage;
}

public enum BossActionType { Melee, Magic, Ultimate, AOE }

public class enemyAI : rpgcharacter {
    public BossType selectedBoss;
    public Sprite RicardioSprite;
    public Sprite algorithmSprite;
    public Sprite lovebombTedSprite;

    private BossStats BS;
    private bool canAttackBoth = true;
    private bool hasSaidOpeningLine = false;
    private System.Random syncedRNG;

    private static readonly Dictionary<BossType, string[]> extraDialogueLines = new() {
        { BossType.Ricardio, new[] { "Love hurts, doesn't it?", "Let me serenade your demise." } },
        { BossType.TheAlgorithm, new[] { "Processing your defeat...", "Feeling seen? That’s just targeted advertising." } },
        { BossType.LovebombTed, new[] { "It's called 'Encyclopaydia'", "I gotta go drop a massive New Jersey" } },
    };

    private static readonly Dictionary<BossType, string> openingLines = new() {
        { BossType.Ricardio, "Your heart will break to my rhythm." },
        { BossType.TheAlgorithm, "Initializing... You won't like the results." },
        { BossType.LovebombTed, "Hey... haaave you met Ted?" }
    };

    private static readonly Dictionary<BossType, string> deathLines = new() {
        { BossType.Ricardio, "You... never loved me..." },
        { BossType.TheAlgorithm, "Error... result... unexpected..." },
        { BossType.LovebombTed, "Maybe I should go back to Robin..." }
    };

    private static readonly Dictionary<BossType, string> winLines = new() {
        { BossType.Ricardio, "Another broken heart for my collection." },
        { BossType.TheAlgorithm, "Your data suggests... utter failure." },
        { BossType.LovebombTed, "Maybe you are the one..." }
    };

    public void SetSeed(int seed) {
        syncedRNG = new System.Random(seed);
    }

    public string GetBossId() => selectedBoss.ToString();

    public void AssignBossById(string id) {
        if (!Enum.TryParse(id, out selectedBoss)) return;
        AssignSelectedBoss();
    }

    public void AssignRandomBoss()
    {
        int bossCount = Enum.GetValues(typeof(BossType)).Length;
        selectedBoss = (BossType)syncedRNG.Next(0, bossCount);

        AssignSelectedBoss();
    }


    public void AssignSelectedBoss(bool applyDefaultHealth = true)
    {
        switch (selectedBoss)
        {
            case BossType.Ricardio:
                BS = BossLibrary.Ricardio;
                break;
            case BossType.TheAlgorithm:
                BS = BossLibrary.TheAlgorithm;
                break;
            case BossType.LovebombTed:
                BS = BossLibrary.LovebombTed;
                break;
        }

        BS.sprite = selectedBoss switch
        {
            BossType.Ricardio => RicardioSprite,
            BossType.TheAlgorithm => algorithmSprite,
            BossType.LovebombTed => lovebombTedSprite,
            _ => null
        };

        var renderer = GetComponent<SpriteRenderer>();
        if (renderer == null || BS.sprite == null) return;

        renderer.sprite = BS.sprite;
        transform.localPosition = BS.position;
        transform.localScale = BS.scale;

        charName = BS.name;
        if (displayName != null) displayName.text = BS.name;

        if (applyDefaultHealth)
        {
            health = BS.maxHealth;
            updateHealthbar();
        }
    }

    public override float MaxHealth => BS.maxHealth;
    protected override float MeleeAttackDam => BS.meleeDamage;
    protected override float MagicAttackDam => selectedBoss == BossType.TheAlgorithm ? BS.magicDamage * 0.6f : BS.magicDamage;
    protected override float UltimateDamage => BS.ultimateDamage;

    private rpgcharacter pickTarget() {
        var aliveCharacters = new List<rpgcharacter>();
        foreach (var character in gamemanager.characterRefs) {
            if (!character.getIsDead())
                aliveCharacters.Add(character);
        }
        if (aliveCharacters.Count == 0) return gamemanager.characterRefs[0];
        return aliveCharacters[syncedRNG.Next(0, aliveCharacters.Count)];
    }

    public BossActionType DecideBossAction(out rpgcharacter target) {
        target = pickTarget();

        float healthRatio = health / MaxHealth;
        float roll = (float)syncedRNG.NextDouble();
        bool ultimateReady = !cooldowns.ContainsKey("Ultimate");
        bool magicReady = !cooldowns.ContainsKey("Magic");

        switch (selectedBoss) {
            case BossType.Ricardio:
                if (healthRatio < 0.5f && ultimateReady) return BossActionType.Ultimate;
                if (magicReady && roll > 0.3f) return BossActionType.Magic;
                break;

            case BossType.TheAlgorithm:
                if (canAttackBoth && roll < BS.aoeChance) return BossActionType.AOE;
                if (magicReady && roll > 0.5f) return BossActionType.Magic;
                break;

            case BossType.LovebombTed:
                if (ultimateReady && roll > 0.5f) return BossActionType.Ultimate;
                if (magicReady && roll > 0.3f) return BossActionType.Magic;
                break;
        }

        return BossActionType.Melee;
    }

    public void ExecuteBossAction(BossActionType actionType, rpgcharacter target, Action onComplete) {
        var dm = gamemanager.dialogueManager;

        TrySayExtraDialogueLine();

        switch (actionType) {
            case BossActionType.AOE:
                PerformAOEAttack();
                break;
            case BossActionType.Ultimate:
                PerformUltimateAttack(target);
                break;
            case BossActionType.Magic:
                PerformMagicAttack(target);
                break;
            case BossActionType.Melee:
                PerformMeleeAttack(target);
                break;
        }

        reduceCooldowns();

        if (BS.healsAfterAction) {
            dm.EnqueueDialogue(new DialogueEntry(
                $"{charName} regains some confidence and heals!",
                () => healHealth(10)
            ));
        }

        if (actionType == BossActionType.AOE) {
            foreach (var player in gamemanager.characterRefs) {
                if (!player.getIsDead()) {
                    var effect = applyPostEffect(player);
                    if (effect != null) dm.EnqueueDialogue(effect);
                }
            }
        } else {
            var effect = applyPostEffect(target);
            if (effect != null) dm.EnqueueDialogue(effect);
        }

        dm.EnqueueDialogue(new DialogueEntry(
            $"{charName} ends their turn.",
            null,
            () => onComplete?.Invoke()
        ));
    }

    private DialogueEntry applyPostEffect(rpgcharacter target) {
        if (BS.appliesBurn && !target.getIsDead() && target.getStatusEffect() == StatusType.none) {
            Array values = Enum.GetValues(typeof(StatusType));
            List<StatusType> validEffects = new List<StatusType>();

            foreach (StatusType val in values) {
                if (val != StatusType.none)
                    validEffects.Add(val);
            }

            StatusType randomEffect = validEffects[syncedRNG.Next(0, validEffects.Count)];
            return new DialogueEntry(
                $"{target.charName} is now {randomEffect}!",
                () => target.applyStatus(randomEffect, 2)
            );
        }

        return null;
    }

    public string GetOpeningLine() {
        if (!hasSaidOpeningLine) {
            hasSaidOpeningLine = true;
            return openingLines.TryGetValue(selectedBoss, out var line) ? line : null;
        }
        return null;
    }

    public string GetDeathLine() => deathLines.TryGetValue(selectedBoss, out var line) ? line : null;
    public string GetWinLine() => winLines.TryGetValue(selectedBoss, out var line) ? line : null;

    private void TrySayExtraDialogueLine() {
        var dm = gamemanager.dialogueManager;

        if (syncedRNG.NextDouble() < 0.4 &&
            extraDialogueLines.TryGetValue(selectedBoss, out var lines) &&
            lines.Length > 0) {
            var line = lines[syncedRNG.Next(0, lines.Length)];
            dm.EnqueueDialogue(new DialogueEntry(line));
        }
    }

    private void PerformAOEAttack() {
        var dm = gamemanager.dialogueManager;
        dm.EnqueueDialogue(new DialogueEntry(
            $"{charName} attacks both players with {BS.AOEName}",
            () => {
                foreach (var player in gamemanager.characterRefs)
                    if (!player.getIsDead()) meleeAttack(player);
            }
        ));
    }

    private void PerformUltimateAttack(rpgcharacter target) {
        var dm = gamemanager.dialogueManager;
        dm.EnqueueDialogue(new DialogueEntry(
            $"{charName} unleashes {BS.ultimateName} on {target.charName}!",
            () => ultimateAttack(target),
            () => cooldowns["Ultimate"] = 3
        ));
    }

    private void PerformMagicAttack(rpgcharacter target) {
        var dm = gamemanager.dialogueManager;
        dm.EnqueueDialogue(new DialogueEntry(
            $"{charName} casts {BS.magicName} on {target.charName}!",
            () => magicAttack(target),
            () => cooldowns["Magic"] = 2
        ));
    }

    private void PerformMeleeAttack(rpgcharacter target) {
        var dm = gamemanager.dialogueManager;
        dm.EnqueueDialogue(new DialogueEntry(
            $"{charName} slashes {target.charName} with {BS.meleeName}!",
            () => meleeAttack(target)
        ));
    }

    public override void died() {
        gamemanager.deathDispatcher(this);
    }

    public int GetNextSeed()
    {
        return syncedRNG.Next(0, 10000);
    }

}