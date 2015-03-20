package ar.com.ksys.ringo.service;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.IBinder;
import android.util.Log;

import java.io.IOException;
import java.net.InetAddress;

import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;

import ar.com.ksys.ringo.service.util.RingoServiceInfo;

public class DiscovererService extends Service {
    private static final String TAG = DiscovererService.class.getSimpleName();

    private String mServiceType;
    private String mServiceName;

    private WifiManager.MulticastLock multicastLock;

    @Override
    public void onCreate() {
        // Acquire a multicast lock, required for DNS service discovery
        WifiManager wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        multicastLock = wifiManager.createMulticastLock("RingoDiscoveryLock");
        multicastLock.setReferenceCounted(true);
        multicastLock.acquire();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        mServiceType = intent.getStringExtra("service_type");
        mServiceName = intent.getStringExtra("service_name");

        new RingoServiceDiscover().execute();

        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        Log.d(TAG, "ServiceDiscoverer destroyed!");
    }

    private class RingoServiceDiscover extends AsyncTask<Void, Void, Void> {
        private JmDNS jmdns;

        @Override
        protected Void doInBackground(Void... params) {
            try {
                jmdns = JmDNS.create(InetAddress.getByName("0.0.0.0"));
                Log.d(TAG, "JmDNS created on " + jmdns.getInterface());
            } catch(IOException e) {
                e.printStackTrace();
            }

            jmdns.addServiceListener(mServiceType, new ServiceListener() {
                @Override
                public void serviceAdded(ServiceEvent serviceEvent) {
                    ServiceInfo info = serviceEvent.getInfo();
                    if(info.getName().contains(mServiceName)) {
                        Log.d(TAG, "Service found");
                        jmdns.requestServiceInfo(serviceEvent.getType(), serviceEvent.getName(), 1);
                    }
                }

                @Override
                public void serviceRemoved(ServiceEvent serviceEvent) {
                    Log.d(TAG, "Service removed");
                }

                @Override
                public void serviceResolved(ServiceEvent serviceEvent) {
                    Log.d(TAG, "Service resolved");

                    ServiceInfo info = serviceEvent.getInfo();
                    Log.d(TAG, "Address 4: " + info.getInet4Addresses().length);
                    Log.d(TAG, "Address 6: " + info.getInet6Addresses().length);
                    Log.d(TAG, "Server: " + info.getServer());
                    Log.d(TAG, "Name: " + info.getName());
                    Log.d(TAG, "QName: " + info.getQualifiedName());
                    Log.d(TAG, "Port: " + info.getPort());
                    Log.d(TAG, "TXT: " + info.getNiceTextString());

                    jmdns.removeServiceListener(mServiceType, this);

                    // Release the beast
                    if(multicastLock != null) {
                        multicastLock.release();
                    }

                    try {
                        jmdns.close();
                    } catch(IOException e) {
                        e.printStackTrace();
                    }

                    Log.d(TAG, "Stopping service discovery");

                    // Start the xmpp service and send it the connection info
                    Intent intent = new Intent(DiscovererService.this,
                                               XmppClientService.class);
                    intent.putExtra("service_info", new RingoServiceInfo(info));
                    startService(intent);

                    // Our work here is done
                    stopSelf();
                }
            });
            return null;
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
