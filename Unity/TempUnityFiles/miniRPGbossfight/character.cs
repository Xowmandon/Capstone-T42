//Author: Benjamin Steinberg
//Created: 12/11/2024
//Notes: not totally sure how to select child classes in run time

using TMPro;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

public enum roster
    {
        Warrior,
        Paladin,
        Mage,
        Healer,
        Enemy,
        none
    }

public class rpgcharacter : MonoBehaviour
{
    //public
    public Image healthbar;

    //private
    private float health;
    private bool isDead = false;

    //test stats
    private float maxHealth = 70;
    private float meleeAttackDam = 10;
    private float magicAttackDam = 45;
    private float healAmount = 40;

    //private
    private RPGManager gamemanager;

    void Awake()
    {
        health = maxHealth;
    }

    public bool getIsDead()
    {
        return isDead;
    }

    public void receiveDamage(float damage)
    {
        health -= damage;
        health = Mathf.Clamp(health, 0f, maxHealth);
        Debug.Log("received damage");
        updateHealthbar();
        if (health == 0)
        {
            isDead = true;
            gamemanager.deathDispatcher(this);
        }
    }

    public void healHealth(float amount)
    {
        health += amount;
        health = Mathf.Clamp(health, 0f, maxHealth);
        updateHealthbar();
    }

    public void meleeAttack(rpgcharacter enemy)
    {
        enemy.receiveDamage(meleeAttackDam);
        gamemanager.gamePanelText(" used Melee Attack!");
        Debug.Log("melee attack");
    }

    public void magicAttack(rpgcharacter enemy)
    {
        enemy.receiveDamage(magicAttackDam);
        gamemanager.gamePanelText(" used Magic Attack!");
    }

    public void healAlly(rpgcharacter ally)
    {
        ally.healHealth(healAmount);
        gamemanager.gamePanelText(" healed their ally!");
    }

    public void updateHealthbar()
    {  
        Debug.Log("fill amount hp bar: " + health/maxHealth);
        healthbar.fillAmount = health/maxHealth;
    }

    public void getGameMan(RPGManager gm)
    {
        gamemanager = gm;
    }

}

//Child Enemy Class
public class Enemy : rpgcharacter
{
    //Private
    private int maxHealth = 120;
    private int meleeAttackDam = 40;
    private int magicAttackDam = 55;
    private int healAmount = 0;
}

//Child Warrior Class
public class Warrior : rpgcharacter
{
    //Private
    private int maxHealth = 100;
    private int meleeAttackDam = 40;
    private int magicAttackDam = 20;
    private int healAmount = 0;
}

//Child Paladin Class
public class Paladin : rpgcharacter
{
    //Private
    private int maxHealth = 140;
    private int meleeAttackDam = 30;
    private int magicAttackDam = 10;
    private int healAmount = 30;
}

//Child Mage Class
public class Mage : rpgcharacter
{
    //Private
    private int maxHealth = 90;
    private int meleeAttackDam = 10;
    private int magicAttackDam = 55;
    private int healAmount = 30;
}

//Child Healer Class
public class Healer : rpgcharacter
{
    //Private
    private int maxHealth = 100;
    private int meleeAttackDam = 1;
    private int magicAttackDam = 35;
    private int healAmount = 50;
}