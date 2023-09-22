package com.algorithms.array;

public class Comparison {
    public static void main(String[] args) {
        String a = "Sejal";
        String b = "Sejal";
        String c = a;
//        System.out.println(c == a);

//        System.out.println(a == b); //if result is true, then the ref variable is pointing to the same object

        
        String name1 = new String("Kunal");
        String name2 = new String("Kunal");
//        System.out.println("Equal to operator: " + name1 == name2);
        System.out.println(".equals method: " + name1.equals(name2));
    }
}
