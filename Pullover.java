package TD1;

public class Pullover {  
    final public static String MARQUE = "M";
    public static String modele;
    private final String taille;
    public double prix;
    private boolean etat; // true = plié false = déplié
    private boolean abime; // true = déchiré false = en bon état
    private String couleur;
    
    public Pullover(String taille,double prix, String couleur)
    {
        this.taille = taille;
        this.etat = false;
        this.abime = false;
        this.prix = prix;
        this.couleur = couleur;
    }
    
    public String getTaille() {return taille;}
    public double getPrix() {return prix;}
    public boolean isPlie() {return etat;}
    public boolean isAbime() {return abime;}
    public String getCouleur() {return couleur;}
    
    public void setPrix(double prix) {this.prix = prix;}
    public void setPlie(boolean etat) {this.etat = etat;}
    public void setString(String couleur) {this.couleur=couleur;}  
    
    @Override
    public String toString()
    {
        return "Pullover(" + MARQUE  + "," + modele + "," + taille + "," + prix + "," + etat + "," + abime + "," + couleur + ")";
    }
    
    public int CompareTo(Pullover other)
    {
        // < 0 : this > other
        // 0 : this == other
        // > 0 : this > other
        return this.couleur.compareTo(other.couleur);
    }
}
