package ar.com.ksys.ringo;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;


public class VisitorActivity extends ActionBarActivity {
    private static final String TAG = VisitorActivity.class.getSimpleName();
    private ImageView visitorPictureView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_visitor);

        visitorPictureView = (ImageView) findViewById(R.id.imageView);

        URL pictureUrl = (URL) getIntent().getSerializableExtra("url");
        new PictureDownloader().execute(pictureUrl);
    }

    private class PictureDownloader extends AsyncTask<URL, Void, Bitmap> {
        @Override
        protected Bitmap doInBackground(URL... urls) {
            URL url = urls[0];
            Bitmap picture = null;
            try {
                HttpURLConnection connection = (HttpURLConnection)
                        url.openConnection();
                InputStream in = new BufferedInputStream(connection.getInputStream());
                picture = BitmapFactory.decodeStream(in);
            } catch(IOException e) {
                Log.e(TAG, "Connection to media server failed");
            }
            return picture;
        }

        @Override
        protected void onPostExecute(Bitmap bitmap) {
            visitorPictureView.setImageBitmap(bitmap);
        }
    }
}
