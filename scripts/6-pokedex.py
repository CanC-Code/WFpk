import os
def create_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name: os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(content)

java_path = "app/src/main/java/com/genesis/pokemon"

# Pokedex XML Layout
create_file("app/src/main/res/layout/activity_pokedex.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" 
    android:layout_width="match_parent" android:layout_height="match_parent" 
    android:orientation="vertical" android:background="#121212" android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" 
        android:text="NATIONAL POKEDEX" android:textColor="#FF0000" android:textSize="24sp" android:textStyle="bold"/>
    <ListView android:id="@+id/pokedex_list" android:layout_width="match_parent" android:layout_height="match_parent" />
</LinearLayout>""")

# Pokedex Java Activity
create_file(f"{java_path}/PokedexActivity.java", """package com.genesis.pokemon;
import android.app.Activity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import org.json.JSONArray;
import java.io.InputStream;
import java.util.ArrayList;

public class PokedexActivity extends Activity {
    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        setContentView(R.layout.activity_pokedex);
        ListView list = findViewById(R.id.pokedex_list);
        ArrayList<String> names = new ArrayList<>();
        try {
            InputStream is = getAssets().open("pokedex.json");
            byte[] buffer = new byte[is.available()];
            is.read(buffer);
            JSONArray array = new JSONArray(new String(buffer));
            for(int i=0; i<array.length(); i++) {
                names.add("#" + array.getJSONObject(i).getInt("id") + " " + array.getJSONObject(i).getString("name"));
            }
        } catch (Exception e) {}
        list.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, names));
    }
}""")
