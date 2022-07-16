import torchtext.legacy.data as data
import torch
import os


def get_datasets(path: str = os.getcwd() + '/data/airline_sentiment_analysis', vocab_size: int = 10000) -> tuple:
    text_field = data.Field(tokenize='spacy', tokenizer_language='en_core_web_sm', lower=True)
    label_field = data.LabelField(dtype=torch.int64)

    dataset = data.TabularDataset(path=path,
                                  fields=[(None, None), ('airline_sentiment', label_field), ('text', text_field)],
                                  format='csv', skip_header=True)
    train_dataset, valid_dataset = dataset.split(split_ratio=0.8)
    text_field.build_vocab(train_dataset, max_size=vocab_size)
    label_field.build_vocab(train_dataset)

    return train_dataset, valid_dataset, text_field, label_field


def get_dataloaders(train_dataset: data.TabularDataset, valid_dataset: data.TabularDataset, batch_size: int = 32,
                    device: torch.device = torch.device('cpu')) -> tuple:
    train_loader, valid_loader = data.BucketIterator.splits([train_dataset, valid_dataset], batch_size=batch_size,
                                                            sort_within_batch=False, device=device,
                                                            sort_key=lambda x: len(x.text))
    return train_loader, valid_loader
