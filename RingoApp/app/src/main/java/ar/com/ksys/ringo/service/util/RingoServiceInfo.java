package ar.com.ksys.ringo.service.util;

import android.os.Parcel;
import android.os.Parcelable;
import java.net.Inet4Address;
import java.net.Inet6Address;

import javax.jmdns.ServiceInfo;

/**
 * Utility class that implements the Parcelable interface for
 * Service Info, similar to Android's NsdServiceInfo
 */
public class RingoServiceInfo  implements Parcelable {
    private String ipv4Address;
    private String ipv6Address;
    private String serviceName;
    private String mucHost;
    private String mucName;
    private int port;

    public RingoServiceInfo(Parcel in) {
        ipv4Address = in.readString();
        ipv6Address = in.readString();
        serviceName = in.readString();
        mucHost = in.readString();
        mucName = in.readString();
        port = in.readInt();
    }

    public RingoServiceInfo(ServiceInfo info) {
        port = info.getPort();
        serviceName = info.getName();
        mucHost = info.getPropertyString("muc_host");
        mucName = info.getPropertyString("muc_name");

        Inet4Address[] ipv4s = info.getInet4Addresses();
        if(ipv4s.length > 0) {
            ipv4Address = ipv4s[0].getHostAddress();
        } else {
            ipv4Address = "";
        }

        Inet6Address[] ipv6s = info.getInet6Addresses();
        if(ipv6s.length > 0) {
            ipv6Address = ipv6s[0].getHostAddress();
        } else {
            ipv6Address = "";
        }
    }

    /**
     * This function returns the IP adress of the service. We can have both,
     * IPv4 and IPv6 adresses. In such case, we prefer the former because
     * connecting with IPv6 requires more work.
     *
     * @return IPv4 or IPv6 adress of the service
     */
    public String getServiceHostAddress() {
        if(ipv4Address.isEmpty())
            return ipv6Address;

        if(ipv6Address.isEmpty())
            return ipv4Address;

        // We have both
        return ipv4Address;
    }

    public String getServiceName() {
        return serviceName;
    }

    /**
     * Construct the room name in the format 'ringo@conference.ringoxmppserver'
     * @return The room the device should join to.
     */
    public String getMucRoom() {
        String room = mucName + "@" + mucHost + "." + serviceName;
        return room.toLowerCase();
    }

    public int getPort() {
        return port;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(ipv4Address);
        dest.writeString(ipv6Address);
        dest.writeString(serviceName);
        dest.writeString(mucHost);
        dest.writeString(mucName);
        dest.writeInt(port);
    }

    public static final Creator<RingoServiceInfo> CREATOR
            = new Creator<RingoServiceInfo>() {

        @Override
        public RingoServiceInfo createFromParcel(Parcel source) {
            return new RingoServiceInfo(source);
        }

        @Override
        public RingoServiceInfo[] newArray(int size) {
            return new RingoServiceInfo[size];
        }
    };
}
