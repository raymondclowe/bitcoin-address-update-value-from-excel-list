# Install uv if not present
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

# Create uv venv if not present
if [ ! -d .venv ]; then
    uv venv
fi

# System dependencies
sudo apt update
sudo apt install -y libsecp256k1-0 gnupg jq

# Get the latest Electrum version from the website
VERSION=$(curl -s https://electrum.org/ | grep -oP 'download\.electrum\.org/\K\d+\.\d+\.\d+' | head -1)
echo "Latest Electrum version: $VERSION"

# Download Electrum tarball and signature
curl -L -o Electrum-${VERSION}.tar.gz https://download.electrum.org/${VERSION}/Electrum-${VERSION}.tar.gz
curl -L -o Electrum-${VERSION}.tar.gz.asc https://download.electrum.org/${VERSION}/Electrum-${VERSION}.tar.gz.asc

# Download and import ThomasV's public key
curl -L -o ThomasV.asc https://raw.githubusercontent.com/spesmilo/electrum/master/pubkeys/ThomasV.asc
gpg --import ThomasV.asc

# Verify the signature
if gpg --verify Electrum-${VERSION}.tar.gz.asc 2>&1 | grep -q "6694D8DE7BE8EE5631BED9502BD5824B7F9470E6"; then
    echo "Signature verification successful."
else
    echo "Signature verification failed!"
    exit 1
fi

# Install Python dependencies
uv add pycryptodomex cryptography

# Install Electrum using uv pip in the activated uv venv
uv pip install ./Electrum-${VERSION}.tar.gz

# Test installation
echo "Successfully installed Electrum version $(uv run electrum --offline version)"

# set daemon
uv run electrum daemon -d

# Test network connection by doing a simple network call
uv run electrum getinfo