PACKER_VERSION=1.11.2
PWN_HOSTNAME=pwnagotchi
PWN_VERSION=master
BASE_IMAGE_URL?=https://raspi.debian.net/daily/raspi_4_trixie.img.xz
BASE_IMAGE_CHECKSUM?=none
ARTIFACT_PREFIX?=pwnagotchi-debian-trixie-64

all: clean install image

langs:
	@for lang in pwnagotchi/locale/*/; do\
		echo "compiling language: $$lang ..."; \
		./scripts/language.sh compile $$(basename $$lang); \
    done

install:
	curl https://releases.hashicorp.com/packer/$(PACKER_VERSION)/packer_$(PACKER_VERSION)_linux_amd64.zip -o /tmp/packer.zip
	unzip /tmp/packer.zip -d /tmp
	sudo mv /tmp/packer /usr/bin/packer
	git clone https://github.com/solo-io/packer-builder-arm-image /tmp/packer-builder-arm-image
	cd /tmp/packer-builder-arm-image && go get -d ./... && go build
	sudo cp /tmp/packer-builder-arm-image/packer-builder-arm-image /usr/bin

image:
	cd builder && sudo /usr/bin/packer build -var "pwn_hostname=$(PWN_HOSTNAME)" -var "pwn_version=$(PWN_VERSION)" -var "base_image_url=$(BASE_IMAGE_URL)" -var "base_image_checksum=$(BASE_IMAGE_CHECKSUM)" pwnagotchi.json
	sudo mv builder/output-pwnagotchi/image $(ARTIFACT_PREFIX)-$(PWN_VERSION).img
	sudo sha256sum $(ARTIFACT_PREFIX)-$(PWN_VERSION).img > $(ARTIFACT_PREFIX)-$(PWN_VERSION).sha256
	sudo zip $(ARTIFACT_PREFIX)-$(PWN_VERSION).zip $(ARTIFACT_PREFIX)-$(PWN_VERSION).sha256 $(ARTIFACT_PREFIX)-$(PWN_VERSION).img

clean:
	rm -rf /tmp/packer-builder-arm-image
	rm -f $(ARTIFACT_PREFIX)-*.zip $(ARTIFACT_PREFIX)-*.img $(ARTIFACT_PREFIX)-*.sha256
	rm -rf builder/output-pwnagotchi  builder/packer_cache
