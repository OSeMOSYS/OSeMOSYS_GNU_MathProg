VERSION := $(shell git describe)
BUILDDIR := osemosys_gnu_mathprog_$(VERSION)

release: $(BUILDDIR).zip

$(BUILDDIR).zip: model_files data_files $(BUILDDIR)/README.md $(BUILDDIR)/LICENSE
	zip -r $(BUILDDIR).zip $(BUILDDIR)

model_files: $(BUILDDIR)/osemosys.txt $(BUILDDIR)/osemosys_short.txt $(BUILDDIR)/osemosys_fast.txt

data_files:	$(BUILDDIR)/simplicity.txt

$(BUILDDIR)/simplicity.txt:	$(BUILDDIR)
	cp tests/simplicity.txt $(BUILDDIR)/simplicity.txt

$(BUILDDIR)/osemosys.txt: $(BUILDDIR)
	cp src/osemosys.txt $(BUILDDIR)/osemosys.txt

$(BUILDDIR)/osemosys_short.txt: $(BUILDDIR)
	cp src/osemosys_short.txt $(BUILDDIR)/osemosys_short.txt

$(BUILDDIR)/osemosys_fast.txt: $(BUILDDIR)
	cp src/osemosys_fast.txt $(BUILDDIR)/osemosys_fast.txt

$(BUILDDIR)/README.md: $(BUILDDIR)
	cp src/README.md $(BUILDDIR)/README.md

$(BUILDDIR)/LICENSE: $(BUILDDIR)
	cp LICENSE $(BUILDDIR)/LICENSE

$(BUILDDIR):
	mkdir -p "$(BUILDDIR)"

.PHONY: clean release migrations all
all: release
clean:
	rm -f $(BUILDDIR).zip
	rm -rf $(BUILDDIR)