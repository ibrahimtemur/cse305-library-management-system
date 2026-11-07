#!/usr/bin/env bash
# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Runs ./mvnw inside the remote Linux VM whose JDK has an empty truststore and an HTTPS proxy (builds a PKCS12 truststore from the VM CA bundle, uses the wagon transport).
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ts="$HOME/.lms/truststore.p12"
if [ ! -s "$ts" ]; then
  mkdir -p "$HOME/.lms" /tmp/lms-ts
  cat > /tmp/lms-ts/MkTrust.java <<'JAVA'
import java.io.*;import java.security.*;
public class MkTrust{public static void main(String[] a)throws Exception{
KeyStore ks=KeyStore.getInstance("PKCS12");ks.load(null,null);int i=0;
try(InputStream in=new FileInputStream(a[0])){for(java.security.cert.Certificate c:java.security.cert.CertificateFactory.getInstance("X.509").generateCertificates(in))ks.setCertificateEntry("c"+i++,c);}
try(OutputStream o=new FileOutputStream(a[1])){ks.store(o,"changeit".toCharArray());}}}
JAVA
  java /tmp/lms-ts/MkTrust.java "${SSL_CERT_FILE:-/etc/ssl/certs/ca-certificates.crt}" "$ts"
fi
opts="-Djavax.net.ssl.trustStore=$ts -Djavax.net.ssl.trustStorePassword=changeit"
if [ -n "${HTTPS_PROXY:-}" ]; then
  hp="${HTTPS_PROXY#*://}"; host="${hp%%:*}"; port="${hp##*:}"; port="${port%%/*}"
  opts="$opts -Dhttps.proxyHost=$host -Dhttps.proxyPort=$port"
fi
export JAVA_TOOL_OPTIONS="$opts"
cd "$repo_root"
exec ./mvnw -Dmaven.resolver.transport=wagon "$@"
