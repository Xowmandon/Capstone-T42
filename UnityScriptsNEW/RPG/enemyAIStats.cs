//Author: Benjamin Steinberg
//Created on: 4/10/2025

using UnityEngine;

public static class BossLibrary
{
    public static readonly BossStats Ricardio = new BossStats
    {
        name = "Ricardio",
        meleeName = "Sonnet Slap",
        magicName = "Tears of Regret",
        AOEName = "Bedrot gasses",
        ultimateName = "Crescendo of Crying",
        appliesBurn = false,
        healsAfterAction = true,
        aoeChance = 0.1f,
        position = new Vector3(1.19f, 0.26f, 0f),
        scale = new Vector3(0.4f, 0.4f, 1f),
        maxHealth = 100,
        meleeDamage = 10,
        magicDamage = 25,
        ultimateDamage = 40
    };

    public static readonly BossStats TheAlgorithm = new BossStats
    {
        name = "The Algorithm",
        meleeName = "Sold your data",
        magicName = "Shadowban Spell",
        AOEName = "Trojan Horse",
        ultimateName = "Targeted Ad Barrage",
        appliesBurn = true,
        healsAfterAction = false,
        aoeChance = 0.4f,
        position = new Vector3(1.14f, -0.26f, 0f),
        scale = new Vector3(0.5f, 0.5f, 1f),
        maxHealth = 120,
        meleeDamage = 12,
        magicDamage = 30,
        ultimateDamage = 50
    };

    public static readonly BossStats LovebombTed = new BossStats
    {
        name = "Ted Mosby",
        meleeName = "Archetecture facts",
        magicName = "Blue French Horn Blast",
        AOEName = "Bad season finale, yikes",
        ultimateName = "LOVEBOMB",
        appliesBurn = true,
        healsAfterAction = true,
        aoeChance = 0.5f,
        position = new Vector3(1.22f, 0.24f, 0f),
        scale = new Vector3(1.1f, 1.1f, 1f),
        maxHealth = 110,
        meleeDamage = 15,
        magicDamage = 28,
        ultimateDamage = 45
    };
}