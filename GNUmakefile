OLD_PACKS=$(patsubst %/about.txt,%,$(wildcard */about.txt))
EGG_PACKS=$(patsubst %/setup.py,%,$(filter-out %HelloWorldZenPack/setup.py, $(wildcard */setup.py)))
BUILD_OLD=$(patsubst %-build,%,$(OLD_PACKS))
BUILD_EGG=$(patsubst %-build,%,$(EGG_PACKS))

ifeq ($(OS),)
OS:=el5
endif


all: build

build: $(BUILD_OLD) $(BUILD_EGG)

$(BUILD_OLD): always
	./build-pack.sh $@ $(OS)

$(BUILD_EGG): always
	./build-egg.sh $@ $(OS)

always:

# I would like to change the name of this target, which just builds and
# doesn't actually install.  Is this used anywhere in the rpath or rpm
# build processes? -jrs
install: build
	mkdir -p $(DESTDIR)/$(ZENHOME)/packs
	for p in $(OLD_PACKS) ; do cp $$p*.zip $(DESTDIR)/$(ZENHOME)/packs ; done
	for p in $(EGG_PACKS) ; do cp $$p*.egg $(DESTDIR)/$(ZENHOME)/packs ; done


install-linked: build
	for p in $(OLD_PACKS) ; do zenpack --link --install $$p ; done
	for p in $(EGG_PACKS) ; do zenpack --link --install $$p ; done

install-normal: build
	for p in $(OLD_PACKS) ; do zenpack --install $$p ; done
	for p in $(EGG_PACKS) ; do zenpack --install $$p ; done

clean:
	for f in $(wildcard *.egg) ; do rm -f $$f ; done
	for f in $(wildcard *.zip) ; do rm -f $$f ; done
	for pat in "build dist temp *.egg-info" ; do \
		for d in $(wildcard */$$pat) ; do rm -rf $$d ; done ; \
	done
