package ar.com.ksys.ringo.service;

import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;
import android.util.Log;

import org.jivesoftware.smack.ConnectionConfiguration;
import org.jivesoftware.smack.MessageListener;
import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.packet.Message;
import org.jivesoftware.smack.tcp.XMPPTCPConnection;
import org.jivesoftware.smack.tcp.XMPPTCPConnectionConfiguration;
import org.jivesoftware.smackx.muc.MultiUserChat;
import org.jivesoftware.smackx.muc.MultiUserChatManager;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;

import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;

import ar.com.ksys.ringo.R;
import ar.com.ksys.ringo.VisitorActivity;
import ar.com.ksys.ringo.service.util.RingoServiceInfo;

public class XmppClientService extends Service {
    private static final String TAG = XmppClientService.class.getSimpleName();

    private SSLContext sslContext;
    private XMPPTCPConnectionConfiguration connectionConfiguration;
    private XMPPTCPConnection connection;
    private MultiUserChat multiUserChat;

    private String mChatRoomName;

    @Override
    public IBinder onBind(Intent intent) {
        throw new UnsupportedOperationException("Not implemented");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
//        if(intent == null) {
//            Log.d(TAG, "Ringo was killed and now is being started again");
//            return START_STICKY;
//        }

        RingoServiceInfo sInfo = intent.getParcelableExtra("service_info");

        initliazeConnection(sInfo.getServiceName(),
                            sInfo.getServiceHostAddress(),
                            sInfo.getPort());

        connection = new XMPPTCPConnection(connectionConfiguration);

        mChatRoomName = sInfo.getMucRoom();

        Log.d(TAG, "CHAT ROOM: " + mChatRoomName);

        new MessageSender().execute();
  //      return START_STICKY;
        return START_REDELIVER_INTENT;
    }

    @Override
    public void onCreate() {
        Log.d(TAG, "Xmpp Service created");
        initializeSSLContext();
    }

    @Override
    public void onDestroy() {
        if(connection.isConnected()) {
            if(multiUserChat.isJoined()) {
                Log.d(TAG, "Leaving chat room");
                try {
                    multiUserChat.leave();
                } catch(SmackException.NotConnectedException e) {
                    e.printStackTrace();
                }
            }
            Log.d(TAG, "Disconnecting from the server");
            new CloseConnection().execute();
        }
        Log.d(TAG, "Ringo service destroyed");
    }

    /**
     * Create a SSLContext that trusts our self-signed certificate
     */
    public void initializeSSLContext() {
        try {
            CertificateFactory cf = CertificateFactory.getInstance("X.509");
            InputStream certFile = new BufferedInputStream(getResources().openRawResource(R.raw.xmpp_cert));
            Certificate ca = cf.generateCertificate(certFile);
            certFile.close();

            // KeyStore containing our trusted CAs
            KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
            keyStore.load(null, null);
            keyStore.setCertificateEntry("ca", ca);

            // TrustManager that trusts the CAs in our KeyStore
            TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
            tmf.init(keyStore);

            sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, tmf.getTrustManagers(), null);
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    private void initliazeConnection(String service, String host, int port) {
        connectionConfiguration = XMPPTCPConnectionConfiguration.builder()
                .setHost(host)
                .setPort(port)
                .setServiceName(service)
                .setUsernameAndPassword("device1", "device1-123")
                .setSecurityMode(ConnectionConfiguration.SecurityMode.required)
                .setCustomSSLContext(sslContext)
                .build();
    }

    private class MessageSender extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            try {
                if(!connection.isConnected()) {
                    Log.d(TAG, "Connecting to XMPP server");
                    connection.connect();
                }

                connection.login();

                multiUserChat = MultiUserChatManager.getInstanceFor(connection)
                        .getMultiUserChat(mChatRoomName);

                multiUserChat.join("Device1");

                multiUserChat.addMessageListener(new MessageListener() {
                    @Override
                    public void processMessage(Message message) {
                        Log.d(TAG, "MENSAJE: " + message);
                        try {
                            JSONObject json = new JSONObject(message.getBody());
                            URL pictureUrl = new URL(json.getString("picture_url"));

                            Intent intent = new Intent(XmppClientService.this, VisitorActivity.class);
                            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                            intent.putExtra("url", pictureUrl);
                            startActivity(intent);
                        } catch (JSONException e) {
                            Log.e(TAG, "Invalid message received. Ignoring");
                        } catch (MalformedURLException e) {
                            Log.e(TAG, "Invalid URL received. There is a problem with the server");
                        }
                    }
                });

                //multiUserChat.sendMessage("Bonjourrrr pedazo de soquetes!");
            } catch(Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    private class CloseConnection extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            connection.disconnect();
            return null;
        }
    }
}
