// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7;

contract ModelStorage {

    struct Model {
        string model_ipfs;
        uint256 accuracy;
        address author;
    }


    Model[] models;


    constructor(
        string memory model_init_ipfs,
        uint256 model_init_accuracy
    ) {
        Model memory tmp = Model({
            model_ipfs: model_init_ipfs,
            accuracy: model_init_accuracy,
            author: msg.sender
        });
        models.push(tmp);
    }


    function submit_model_weight(
        string memory current_model,
        uint256 accuracy_
    ) public {
        Model memory submit_ = Model({
            model_ipfs: current_model,
            accuracy: accuracy_,
            author: msg.sender
        });

        models.push(submit_);
    }


    function get_latest_model_ipfs()
        public
        view
        returns (string memory)
    {
        return models[models.length - 1].model_ipfs;
    }


    function get_all_round() public view returns (Model[] memory) {
        return models;
    }
}