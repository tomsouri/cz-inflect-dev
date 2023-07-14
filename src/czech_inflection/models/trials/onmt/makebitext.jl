function tobitext(fn)
    data = []
    for line in eachline(fn)
        lemma, inflected, features = split(line, '\t')
        features = split(features, ';')
        src = "$(join(lemma, ' ')) # $(join(features, ' '))"
        tgt = join(inflected, ' ')

        push!(data, (src, tgt))
    end
    return data
end

function writelines(fn, lines)
    open(fn, "w") do fout
        for line in lines
            println(fout, line)
        end
    end
end

function main()
    train_file = ARGS[1]
    dev_file = ARGS[2]
    test_file = ARGS[3]

    train = tobitext(train_file)
    dev = tobitext(dev_file)
    test = tobitext(test_file)

    if !isdir("data")
        mkdir("data")
    end
    writelines("data/train.src", [src for (src, tgt) in train])
    writelines("data/train.tgt", [tgt for (src, tgt) in train])
    writelines("data/dev.src", [src for (src, tgt) in dev])
    writelines("data/dev.tgt", [tgt for (src, tgt) in dev])
    writelines("data/test.src", [src for (src, tgt) in test])
    writelines("data/test.tgt", [tgt for (src, tgt) in test])
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end