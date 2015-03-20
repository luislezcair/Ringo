package ar.com.ksys.ringo;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import ar.com.ksys.ringo.service.XmppClientService;
import ar.com.ksys.ringo.service.DiscovererService;


public class MainActivity extends ActionBarActivity {
    //private static final String TAG = MainActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button buttonConnect = (Button) findViewById(R.id.buttonConnect);
        buttonConnect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this,
                                           DiscovererService.class);
                intent.putExtra("service_type", "_xmpp-server._tcp.local.");
                intent.putExtra("service_name", "RingoXMPPServer");
                startService(intent);
            }
        });

        Button buttonStopService = (Button) findViewById(R.id.buttonStopService);
        buttonStopService.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, XmppClientService.class);
                stopService(intent);
            }
        });
    }
}
